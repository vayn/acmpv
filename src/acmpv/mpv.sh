#!/bin/bash
mpv --autofit 950x540 --cache-file TMP --framedrop vo --vf 'lavfi="fps=fps=60:round=down"' $@
