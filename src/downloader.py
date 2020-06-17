from __future__ import unicode_literals
import gzip
import os
import bs4
import sys
import requests
import string
import argparse
import json
from pulled import *
from exported import *
from printer import *


APISETTINGS = {
    "oped": ["OP", "ED"],
    "site parse": "https://animethemes-api.herokuapp.com/id/{0}/",
    "audio site": "https://animethemes-api.herokuapp.com/id/{0}/{1}/audio",
    "filetypes": {"audio": ".mp3", "video": ".webm"}
}


def api_check_errors(malid):

    site = APISETTINGS["site parse"].format(malid)
    try:
        data = requests.get(site).json()
    except:
        fprint("Error", f"API error: {malid} does bot have an entry in {site}")
        return

    if "name" not in data:
        fprint("Error", f"API error: {malid} has an empty entry in {site}")
        return

    return data


def api_parse(malid, download_HD=False, download_audio=False, ignore_already_downloaded=False, preferred_version=1, folder='.'):
    data = api_check_errors(malid)
    if data is None:
        return []

    try:
        os.mkdir(folder)
    except:
        pass
    already_downloaded = os.listdir(folder)

    fprint("parse", malid)

    anime_name = data["name"]
    for song in data["themes"]:
        song_type_version = song["type"]
        if ' ' in song_type_version:
            song_type, version = song_type_version.split(' ')
            version = int(version[1:])
            if version != preferred_version:
                continue
        else:
            song_type = song_type_version

        title = song["title"]
        video_is_hd = False
        if download_audio:
            mirror = APISETTINGS["audio site"].format(malid, song_type_version)
            filetype = APISETTINGS["filetypes"]["audio"]
        else:
            mirror = song["mirror"]
            if len(mirror) > 1:
                mirror = mirror[download_HD]["mirrorUrl"]
                video_is_hd = download_HD
            else:
                mirror = mirror[0]["mirrorUrl"]
            filetype = APISETTINGS["filetypes"]["video"]

        filename = f"{anime_name} {song_type} ({title}){' HD' if video_is_hd else ''}"
        filename += filetype
        filename = ''.join(
            char for char in filename if char in string.printable)

        if ignore_already_downloaded:
            if filename in already_downloaded:
                continue

        yield mirror, filename


def download_anime(site, filename, folder="."):
    try:
        response = requests.get(site, allow_redirects=True)
    except:
        return f"No file found at {site}"
    if response.status_code != 200:
        return f"{response.status_code} in {site}"
    filename = f'{folder}/{filename}'

    with open(filename, 'wb') as file:
        for chunk in response:
            file.write(chunk)
    return False


def main(
    export_file=None,
    mal_username=None,
    folder='.',
    ignore_already_downloaded=False,
    minimum_score=0,
    exclude_dropped=True, exclude_planned=True,
    exclude_anime=[],
    download_audio=False,
    download_HD=False,
    preferred_version=1,
):
    fprint("start","Launching program")
    if mal_username is None:
        data = open_export_file(export_file)

        fprint("read", f"reading file")
        data = get_all_anime_data(data)

        fprint("read", f"getting anime names")
        for malid in filter_anime(data, minimum_score, exclude_dropped, exclude_planned, exclude_anime):

            for site, filename in api_parse(malid, download_HD, download_audio, ignore_already_downloaded, preferred_version, folder):

                fprint("download", filename)
                response = download_anime(site, filename, folder)
                if response:
                    fprint("Error", f"connection/API error: {response}")

    else:
        fprint("read", f"reading anime list of {mal_username}")
        data = get_data_from_mal(mal_username)

        fprint("read", f"getting anime names")
        for malid in website_filter_anime(data, minimum_score, exclude_dropped, exclude_planned, exclude_anime):

            for site, filename in api_parse(malid, download_HD, download_audio, ignore_already_downloaded, preferred_version, folder):

                fprint("download", filename)
                response = download_anime(site, filename, folder)
                if response:
                    fprint("Error", f"connection/API error: {response}")


def get_parser():
    parser = argparse.ArgumentParser(description="""
Download anime openings and endings using your AML username or a MAL export file and animethemes.moe.
By searching through your animelist and picking out every anime, this program finds all of your liked anime.
It then parses it and using an animethemes.moe api finds all anime OP's and ED's.
It then downloads it in either mp3 or webm file format, allowing you to get that weeb shit you deserve.
""")
    parser.add_argument('-f', metavar='export', type=str, default=None,
                        help='MAL export file, can be zipped or unzipped.')
    parser.add_argument('-u', metavar='username', type=str, default=None,
                        help='MAL export file, can be zipped or unzipped.')
    parser.add_argument('-F', metavar='folder', type=str, default='.',
                        help='Folder to save the integers into.')
    parser.add_argument('--s', metavar='skip', type=bool, default=False, const=True, nargs='?',
                        help='Skip songs that are already downloaded.')
    parser.add_argument('-m', metavar='min_score', type=int, default=0,
                        help='Minimum score that has to be given to a show to be downloaded.')
    parser.add_argument('--d', metavar='dropped', type=bool, default=True, const=False, nargs='?',
                        help='Include anime that has been dropped.')
    parser.add_argument('--p', metavar='planned', type=bool, default=True, const=False, nargs='?',
                        help='Include anime that hasn\'t been watched yet.')
    parser.add_argument('--a', metavar='audio', type=bool, default=False, const=True, nargs='?',
                        help='Download mp3 instead of video.')
    parser.add_argument('--q', metavar='quality', type=bool, default=False, const=True, nargs='?',
                        help='Download videos in higher quality.')
    parser.add_argument('-v', metavar='preferred_version', type=int, default=1,
                        help='Preferred version to download, used to download openings that otherwise cause problems')
    parser.add_argument('-e', metavar='excluded', type=str, nargs='+', default=[],
                        help='All anime that should be excluded from download, can be also MAL id.')

    return parser


def convert_args(args):
    if args.a and args.q:
        raise ValueError("Cannot download HD audio files.")
    elif args.f is not None and args.u is not None:
        raise ValueError(
            "Cannot search myanimelist.net and read a file at the same time.")
    return {
        'export_file': args.f,
        'mal_username': args.u,
        'folder': args.F,
        'ignore_already_downloaded': args.s,
        'minimum_score': args.m,
        'exclude_dropped': args.d,
        'exclude_planned': args.p,
        'exclude_anime': args.e,
        'download_audio': args.a,
        'download_HD': args.q,
        'preferred_version': args.v
    }


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args(sys.argv[1:])
    args = convert_args(args)
    main(**args)