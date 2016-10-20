#!/usr/bin/env python3
import logging
from . import downloaders as DS
from .you_get import common


def get_domain(url):
    try:
        video_host = common.r1(r'https?://([^/]+)/', url)
        video_url = common.r1(r'https?://[^/]+(.*)', url)
        assert video_host and video_url
    except:
        raise Exception('域名格式错误')

    if video_host.endswith('.com.cn'):
        video_host = video_host[:-3]
    domain = common.r1(r'(\.[^.]+\.[^.]+)$', video_host) or video_host
    assert domain, 'unsupported url: ' + url

    domain = common.r1(r'([^.]+)', domain)
    return domain

def main():
    import os
    import subprocess
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="视频网址")
    parser.add_argument("-f", "--format", dest="format", help="指定视频格式")
    parser.add_argument("-i", "--info", action="store_true", help="查看视频信息")
    args = parser.parse_args()

    rootpath = os.path.dirname(os.path.realpath(__file__))
    make_path = lambda f: os.path.join(rootpath, f)

    url = args.url
    domain = get_domain(url)

    dansites = {'a': 'acfun', 'b': 'bilibili'}
    isDansite = True if (domain in dansites.values()) else False
    title = 'acmpv'
    ass = ''

    if isDansite:
        if domain in dansites['a']:
            downloader = DS.AcfunAssDownloader(url)
        elif domain in dansites['b']:
            downloader = DS.BiliAssDownloader(url)
        title, ass = downloader.download()

    mpv = [make_path('mpv.sh'), '--force-media-title', title.replace(' ', '_')]
    mpv += ['--merge-files', '--no-video-aspect']
    if isDansite: mpv += ['--sub-ass', '--sub-file', ass]
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
