# -*- coding: utf8 -*-
# SPDX-License-Identifier: CECILL-2.1
"""
Save Matplotlib figure. Optimize PNG format using PIL.

:copyright:
    2022-2023 Claudio Satriano <satriano@ipgp.fr>
:license:
    CeCILL Free Software License Agreement v2.1
    (http://www.cecill.info/licences.en.html)
"""
import io
import PIL
import logging
import warnings
# Reduce logging level for PIL to avoid DEBUG messages
pil_logger = logging.getLogger('PIL')
pil_logger.setLevel(logging.WARNING)
# Reduce logging level for fontTools to avoid DEBUG messages
mpl_logger = logging.getLogger('fontTools')
mpl_logger.setLevel(logging.WARNING)
# Silence PIL warnings about transparency needing RGBA, since we remove the
# alpha channel anyway (see below)
warnings.filterwarnings('ignore', message='Palette images with Transparency')


def savefig(fig, figfile, fmt, quantize_colors=True, **kwargs):
    """Save Matplotlib figure. Optimize PNG format using PIL."""
    if fmt == 'png':
        buf = io.BytesIO()
        fig.savefig(buf, format='png', **kwargs)
        buf.seek(0)
        img = PIL.Image.open(buf)
        if quantize_colors:
            img = img.convert('P', palette=PIL.Image.ADAPTIVE, colors=256)
        else:
            # just remove the alpha channel
            img = img.convert('RGB')
        img.save(figfile, optimize=True)
        img.close()
    else:
        fig.savefig(figfile, **kwargs)
