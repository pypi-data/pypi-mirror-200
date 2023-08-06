import argparse
import json
import re
import string
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

import whosyouragent
from noiftimer import Timer
from printbuddies import ProgBar

root = Path(__file__).parent


def clean_string(text: str) -> str:
    """Remove punctuation and trailing spaces from text."""
    return re.sub(f"[{re.escape(string.punctuation)}]", "", text).strip()


@dataclass
class Track:
    title: str
    number: int
    url: str

    def __post_init__(self):
        self.title = clean_string(self.title)

    @property
    def numbered_title(self):
        num = str(self.number)
        if len(num) == 1:
            num = "0" + num
        return f"{num} - {self.title}"


@dataclass
class Album:
    url: str
    artist: str = None
    title: str = None
    tracks: list[Track] = None
    art_url: str = None

    def __repr__(self):
        return f"{self.title} by {self.artist}"

    def __post_init__(self):
        response = requests.get(self.url, headers=whosyouragent.get_agent(as_dict=True))
        if response.status_code != 200:
            raise RuntimeError(
                f"Getting album info failed with code {response.status_code}"
            )
        soup = BeautifulSoup(response.text, "html.parser")
        self.art_url = soup.find("meta", attrs={"property": "og:image"}).get("content")
        for script in soup.find_all("script"):
            if script.get("data-cart"):
                data = script
                break
        data = json.loads(data.attrs["data-tralbum"])
        self.artist = clean_string(data["artist"])
        self.title = clean_string(data["current"]["title"])
        self.tracks = [
            Track(track["title"], track["track_num"], track["file"]["mp3-128"])
            for track in data["trackinfo"]
            if track.get("file")
        ]


class AlbumRipper:
    def __init__(
        self, album_url: str, no_track_number: bool = False, overwrite: bool = False
    ):
        """
        :param no_track_number: If True, don't add the track
        number to the front of the track title."""
        self.album = Album(album_url)
        self.no_track_number = no_track_number
        self.overwrite = overwrite

    def make_save_path(self):
        self.save_path = Path.cwd() / self.album.artist / self.album.title
        self.save_path.mkdir(parents=True, exist_ok=True)

    @property
    def headers(self) -> dict:
        """Get a headers dict with a random useragent."""
        return whosyouragent.get_agent(as_dict=True)

    def save_track(self, track_title: str, content: bytes) -> Path:
        """Save track to self.save_path/{track_title}.mp3.
        Returns the Path object for the save location.

        :param content: The binary data of the track."""
        file_path = self.save_path / f"{track_title}.mp3"
        file_path.write_bytes(content)
        return file_path

    def get_track_content(self, track_url: str) -> bytes:
        """Make a request to track_url and return the content.
        Raises a RunTimeError exception if response.status_code != 200."""
        response = requests.get(track_url, headers=self.headers)
        if response.status_code != 200:
            raise RuntimeError(
                f"Downloading track failed with status code {response.status_code}."
            )
        return response.content

    def download_album_art(self):
        """Download the album art and save as a .jpg."""
        file_path = self.save_path / f"{self.album.title}.jpg"
        try:
            response = requests.get(self.album.art_url, headers=self.headers)
            file_path.write_bytes(response.content)
        except Exception as e:
            print(f"Failed to download art for {self.album}.")
            print(e)

    def track_exists(self, track: Track) -> bool:
        """Return if a track already exists in self.save_path."""
        path = self.save_path / (
            track.title if self.no_track_number else track.numbered_title
        )
        return path.with_suffix(".mp3").exists()

    def rip(self):
        """Download and save the album tracks and album art."""
        if len(self.album.tracks) == 0:
            print(f"No public tracks available for {self.album}.")
            return None
        self.make_save_path()
        self.download_album_art()
        bar = ProgBar(len(self.album.tracks) - 1, width_ratio=0.5)
        bar.timer.subsecond_resolution = True
        fails = []
        if not self.overwrite:
            self.album.tracks = [
                track for track in self.album.tracks if not self.track_exists(track)
            ]
        for track in self.album.tracks:
            bar.display(
                suffix=f"Downloading {track.title}",
                counter_override=1 if len(self.album.tracks) == 1 else None,
            )
            try:
                content = self.get_track_content(track.url)
                self.save_track(
                    track.title if self.no_track_number else track.numbered_title,
                    content,
                )
            except Exception as e:
                fails.append((track, str(e)))
        print(f"Finished downloading {self.album} in {bar.timer.elapsed_str}.")
        if fails:
            print("The following tracks failed to download:")
            for fail in fails:
                print(f"{fail[0].title}: {fail[1]}")


class BandRipper:
    def __init__(
        self, band_url: str, no_track_number: bool = False, overwrite: bool = False
    ):
        self.band_url = band_url
        self.albums = []
        for url in self.get_album_urls(band_url):
            try:
                self.albums.append(AlbumRipper(url, no_track_number, overwrite))
            except Exception as e:
                print(e)

    def get_album_urls(self, band_url: str) -> list[str]:
        """Get album urls from the main bandcamp url."""
        print(f"Fetching discography from {band_url}...")
        response = requests.get(band_url, headers=whosyouragent.get_agent(as_dict=True))
        if response.status_code != 200:
            raise RuntimeError(
                f"Getting {band_url} failed with status code {response.status_code}."
            )
        soup = BeautifulSoup(response.text, "html.parser")
        grid = soup.find("ol", attrs={"id": "music-grid"})
        parsed_url = urlparse(band_url)
        base_url = f"https://{parsed_url.netloc}"
        return [base_url + album.a.get("href") for album in grid.find_all("li")]

    def rip(self):
        print(
            f"Downloading {len(self.albums)} albums by {self.albums[0].album.artist}."
        )
        timer = Timer(subsecond_resolution=True)
        timer.start()
        fails = []
        for album in self.albums:
            try:
                album.rip()
            except Exception as e:
                fails.append((album, e))
        timer.stop()
        artist = self.albums[0].album.artist
        print(
            f"Finished downloading {len(self.albums)} albums by {artist} in {timer.elapsed_str}."
        )
        if fails:
            print(f"The following downloads failed:")
            for fail in fails:
                print(f"{fail[0]}: {fail[1]}")


def page_is_discography(url: str) -> bool:
    """Returns whether the url is to a discography page or not."""
    response = requests.get(url, headers=whosyouragent.get_agent(as_dict=True))
    if response.status_code != 200:
        raise RuntimeError(
            f"Getting {url} failed with status code {response.status_code}."
        )
    soup = BeautifulSoup(response.text, "html.parser")
    # Returns None if it doesn't exist.
    grid = soup.find("ol", attrs={"id": "music-grid"})
    if grid:
        return True
    return False


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "urls",
        type=str,
        nargs="*",
        help=""" The bandcamp url(s) for the album or artist.
            If the url is to an artists main page,
            all albums will be downloaded.
            The tracks will be saved to a subdirectory of
            your current directory.
            If a track can't be streamed (i.e. private) it
            won't be downloaded. Multiple urls can be passed.""",
    )

    parser.add_argument(
        "-n",
        "--no_track_number",
        action="store_true",
        help=""" By default the track number will be added
        to the front of the track title. Pass this switch
        to disable the behavior.""",
    )

    parser.add_argument(
        "-o",
        "--overwrite",
        action="store_true",
        help=""" Pass this flag to overwrite existing files.
        Otherwise don't download tracks that already exist locally.""",
    )

    args = parser.parse_args()
    args.urls = [url.strip("/") for url in args.urls]

    return args


def main(args: argparse.Namespace = None):
    if not args:
        args = get_args()
    for url in args.urls:
        if page_is_discography(url):
            ripper = BandRipper(url, args.no_track_number, args.overwrite)
        else:
            ripper = AlbumRipper(url, args.no_track_number, args.overwrite)
        ripper.rip()


if __name__ == "__main__":
    main(get_args())
