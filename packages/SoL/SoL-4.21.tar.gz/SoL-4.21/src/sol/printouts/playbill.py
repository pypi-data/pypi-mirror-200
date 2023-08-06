# -*- coding: utf-8 -*-
# :Project:   SoL — Tourney playbill
# :Created:   dom 22 gen 2023, 18:00:43
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2023 Lele Gaifax
#

from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, Spacer

from ..i18n import gettext

from . import subtitle_style
from .basic import TourneyPrintout


class PlaybillPrintout(TourneyPrintout):
    "Tourney playbill."

    showBoundary = False

    def __init__(self, output, locale, tourney):
        super().__init__(output, locale, tourney, 1)

    def getSubTitle(self):
        return ""

    def execute(self, request):
        """Create and build the document.

        :param request: the Pyramid request instance
        """

        # Superclass draws the QRCode in the title frame
        self.lit_url = None
        self._lit_url = self.getLitURL(request)
        self.createDocument()
        self.doc.build(list(self.getElements()))

    def getElements(self):
        yield from super().getElements()

        url = self._lit_url
        if not url:
            return
        qrcode_width = 10*cm
        drawing = Drawing(qrcode_width, qrcode_width)
        drawing.hAlign = 'CENTER'
        drawing.add(QrCodeWidget(value=url, barWidth=qrcode_width, barHeight=qrcode_width))
        yield drawing
        yield Spacer(0, 1*cm)
        yield Paragraph(gettext('Scan the QRCode and visit the URL to follow'
                                ' the tournament live!'), subtitle_style)
