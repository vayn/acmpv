#!/usr/bin/env python3
import re
import io
import json
import math
import logging
import tempfile
import tkinter as tk

from . import danmaku2ass
from .you_get.common import get_html, r1


def get_srt_json(id):
    url = 'http://danmu.aixifan.com/V2/%s' % id
    return get_html(url)

def get_screent_size():
    root = tk.Tk()
    root.withdraw()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    return [screen_width, screen_height]

def ass_download(url):
    assert re.match(r'http://[^\.]+.acfun.[^\.]+/\D/\D\D(\d+)', url)
    html = get_html(url)

    title = r1(r'data-title="([^"]+)"', html)
    vid = r1('data-vid="(\d+)"', html)
    screen_size = get_screent_size()

    cmt = get_srt_json(vid)
    cmt_in = io.StringIO(cmt)
    cmt_out = tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='\r\n', prefix='tmp-danmaku2ass-', suffix='.ass', delete=False)

    d2a_args = {
        'stage_width': screen_size[0],
        'stage_height': screen_size[1],
        'font_face': 'SimHei',
        'font_size': math.ceil(screen_size[1]/21.6),
        'text_opacity': 0.8,
        'duration_marquee': min(max(6.75*screen_size[0]/screen_size[1]-4, 3.0), 9.0),
        'duration_still': 5.0
    }
    try:
        danmaku2ass.Danmaku2ASS(input_files=[cmt_in], input_format='Acfun', output_file=cmt_out, **d2a_args)
    except Exception as e:
        print('Danmaku2ASS failed, comments are disabled.')
    cmt_out.flush()
    cmt_out.close()

    return [title, cmt_out.name]

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
    title, ass = ass_download(url)

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
