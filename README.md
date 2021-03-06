# what's this project
This project allows you to automaticaly download opening and ending songs from all of your favorite anime without the need of downoading everything yourself. Since almost every weeb uses MAL to track the anime he's watching, this tool is really useful, as every information you need to give it has been written down already. All you need to do is to enter your [MAL](https://myanimelist.net) or [AniList](https://anilist.co) username or just  [export your MAL list](https://myanimelist.net/panel.php?go=export) . You can just run it freely from console. If you want to change some settings, look at `python downloader.py -h`
# disclaimer
All videos are downloaded from animethemes.moe and originally belong to studios who made them. You are not allowed to distribute any videos downloaded, unless you have permission from the studios that made it and animethemes.moe.
Note that owning and distributing the program itself is allowed.
# how to install
- clone this repository or download `src`
- do `pip install  -r requirements.txt` to install all required libraries
# usage
1) enter your mal username or export your animelist and place it into the same folder as downloader.py
2) set the name of a folder you want to save to, defaults to saving in the same folder as downloader.py
3) set wheter you want video, HD video (`--q`) or audio (`--a`)
4) if any videos are broken, you can try chnaging versions `--v` and any videos with an alternative will download instead
# arguments
```arg
usage: downloader.py [-h] [-f export] [-mal mal_username] [-al al_username] [-F folder] [--s [skip]]
                     [-m min_score] [-pr min_priority] [--d [dropped]] [--p [planned]] [--a [audio]]
                     [--q [quality]] [-v preferred_version] [-e excluded [excluded ...]]
                     [-bc banned_chars] [--ascii [only_ascii_chars]] [-ml max_file_lenght]

Download anime openings and endings using your AML username or a MAL export file and
animethemes.moe. By searching through your animelist and picking out every anime, this program finds
all of your liked anime. It then parses it and using an animethemes.moe api finds all anime OP's and
ED's. It then downloads it in either mp3 or webm file format, allowing you to get that weeb shit you
deserve.

optional arguments:
  -h, --help            show this help message and exit
  -f export             MAL export file, can be zipped or unzipped.
  -mal mal_username     MAL username, used to pull data from MAL
  -al al_username       AniList username, used to pull data from AniList
  -F folder             Folder to save the songs into.
  --s [skip]            Skip songs that are already downloaded.
  -m min_score          Minimum score that has to be given to a show to be downloaded.
  -pr min_priority      Minimum priority that has to be given to a show to be downloaded, only with
                        MAL. (Low=1,Normal=2,High=3)
  --d [dropped]         Include anime that has been dropped
  --p [planned]         Inclu de anime that hasn't been watched yet.
  --a [audio]           Download mp3 instead of video.
  --q [quality]         Download videos in higher quality.
  -v preferred_version  Preferred version to download, used to download openings that otherwise
                        cause problems
  -e excluded [excluded ...]
                        All anime that should be excluded from download, can be also MAL id.
  -bc banned_chars      All banned characters, defaults to /, because you are currently using a
                        Linux os
  --ascii [only_ascii_chars]
                        Creates files with only ascii characters in the name.
  -ml max_file_lenght   Limits the lenght of a file (excluding the extension), mostly good for Mac.
```
> ran on Linux

my personal settings if you don't know what to do:
- AUDIO: `-mal="sadru" -F="audio" --a --s`
- VIDEO: `-mal="sadru" -F="video" --q --s`
# TODO
- smarter file recognition
- code optimizations
- network optimizations
- colored printing
- higher usability with importing
- download only one song
