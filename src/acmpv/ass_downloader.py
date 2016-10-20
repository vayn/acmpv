#!/usr/bin/env python3
import io
import math
import tempfile
import tkinter as tk

from . import danmaku2ass
from .you_get.common import get_html, r1
from .you_get.extractors import acfun, bilibili


class AssDownloader:
    def __init__(self):
        self.screen_width = 0
        self.screen_height = 0
        self.d2a_args = {}
        self._init()

    def _init(self):
        self._get_screen_size()
        self.d2a_args = {
            'stage_width': self.screen_width,
            'stage_height': self.screen_height,
            'font_face': 'SimHei',
            'font_size': math.ceil(self.screen_height / 21.6),
            'text_opacity': 0.8,
            'duration_marquee': min(max(6.75 * self.screen_width / self.screen_height - 4, 3.0), 9.0),
            'duration_still': 5.0
        }

    def download(self):
        pass

    def _get_ass(self, comment, comment_format):
        comment_in = io.StringIO(comment)
        comment_out = tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='\r\n', prefix='tmp-danmaku2ass-',
                                                  suffix='.ass', delete=False)
        try:
            danmaku2ass.Danmaku2ASS(input_files=[comment_in], input_format=comment_format, output_file=comment_out,
                                    **self.d2a_args)
        except Exception:
            print('Danmaku2ASS failed, comments are disabled.')
        comment_out.flush()
        comment_out.close()
        return comment_out.name

    def _get_screen_size(self):
        root = tk.Tk()
        root.withdraw()
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        root.destroy()


class AcfunAssDownloader(AssDownloader):
    def __init__(self, url):
        super().__init__()
        self.url = url

    def download(self):
        html = get_html(self.url)
        title = r1(r'data-title="([^"]+)"', html)
        vid = r1('data-vid="(\d+)"', html)

        comment = acfun.get_srt_json(vid)
        ass = self._get_ass(comment, comment_format="Acfun")

        return [title, ass]

