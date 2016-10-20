#!/usr/bin/env python
import sys

if sys.version_info[0] == 3:
    from .__main__ import *
else:
    pass


__version__ = "1.0.3"

__title__ = "acmpv"
__description__ = "Play Acfun video with danmaku in mpv media player"
__uri__ = "https://github.com/Vayn/acmpv"
__doc__ = __description__ + " <" + __uri__ + ">"

__author__ = "Vayn a.k.a VT"
__email__ = "vayn@vayn.de"

__license__ = "WTFPL 2"
__copyright__ = "Copyright (c) 2016 Vayn a.k.a VT"
