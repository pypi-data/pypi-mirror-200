# bandripper

Rip albums from bandcamp using the command line.<br>
Only works for public tracks.<br>
Quality is limited to mp3 at 128 kbps.

## Installation

Install with:

<pre>
pip install bandripper
</pre>



## Usage

##### Options
<pre>
>bandripper -h
usage: bandripper [-h] [-n] [-o] [urls ...]

positional arguments:
  urls                  The bandcamp url(s) for the album or artist. If the url is to an artists main page, all albums will be downloaded. The tracks will be saved to a subdirectory of your current directory. If a track can't be streamed (i.e. private) it won't be downloaded.
                        Multiple urls can be passed.

options:
  -h, --help            show this help message and exit
  -n, --no_track_number
                        By default the track number will be added to the front of the track title. Pass this switch to disable the behavior.
  -o, --overwrite       Pass this flag to overwrite existing files. Otherwise don't download tracks that already exist locally.
</pre>
e.g.
<pre>
>bandripper https://blacklungwinter.bandcamp.com/releases
 [______________________________________________________________________________________________________________]-100.00% Downloading Uproot
Finished downloading Bodies of EarthHearts of Space by Blacklung Winter in 3s 107ms 7us.
>dir "./Blacklung Winter/Bodies of EarthHearts of Space"
03/22/2023  01:46 PM           228,335 Bodies of EarthHearts of Space.jpg
03/22/2023  01:46 PM         3,008,887 01 - Bodies of EarthHearts of Space.mp3
03/22/2023  01:46 PM         3,441,057 02 - Dead in the Water.mp3
03/22/2023  01:46 PM         2,792,802 03 - Yin and Yang.mp3
03/22/2023  01:46 PM         3,326,954 04 - Neurotoxin.mp3
03/22/2023  01:46 PM         3,836,446 05 - Uproot.mp3
</pre>
