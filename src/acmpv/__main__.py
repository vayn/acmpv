#!/usr/bin/env python3
import logging
from . import downloaders as DS


def main():
    import os
    import subprocess
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Acfun视频网址")
    parser.add_argument("-f", "--format", dest="format", help="指定视频格式")
    parser.add_argument("-i", "--info", action="store_true", help="查看视频信息")

    args = parser.parse_args()

    url = args.url
    title, ass = DS.AcfunAssDownloader(url).download()

    rootpath = os.path.dirname(os.path.realpath(__file__))
    make_path = lambda f: os.path.join(rootpath, f)

    mpv = [make_path('mpv.sh'), '--force-media-title', title.replace(' ', '_')]
    mpv += ['--merge-files']
    mpv += ['--no-video-aspect', '--sub-ass', '--sub-file', ass]
    mpv += ['--']
    mpv = ' '.join(mpv)

    cmd = [make_path("you-get")]
    if args.info:
        cmd.extend(["-i", url])
    else:
        cmd.extend(["-p", mpv, url])
        if args.format:
            cmd.insert(1, "--format=%s" % args.format)

    player_process = subprocess.Popen(cmd)
    try:
        player_process.wait()
    except KeyboardInterrupt:
        logging.info('Terminating media player...')
        try:
            player_process.terminate()
            try:
                player_process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                logging.info('Killing media player by force...')
                player_process.kill()
        except Exception:
            pass
        raise


if __name__ == '__main__':
    main()
