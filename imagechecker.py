# Gideon Marsh
# github.com/GideonMarsh

from PIL import Image
from math import floor


class ImageChecker:
    def __init__(self):
        self.gopix1 = None
        self.gopix2 = None
        self.gopix3 = None
        self.winpix = None

    def imageSetup(self):
        self.gopix1 = Image.open('images/respawn_air_man_1.png').load()
        self.gopix2 = Image.open('images/respawn_air_man_2.png').load()
        self.gopix3 = Image.open('images/respawn_air_man_3.png').load()
        self.winpix = Image.open('images/level_complete_normal.png').load()

    def checkGameOver(self, image=None, xp=266, yp=200):
        pix = image.load()

        xOffset = floor(image.width / xp)
        yOffset = floor(image.height / yp)
        xShift = floor((image.width % xp) / 2)
        yShift = floor((image.height % yp) / 2)

        for i in range(xp):
            for j in range(yp):
                if (pix[(i * xOffset) + xShift, (j * yOffset) + yShift] != self.gopix1[(i * xOffset) + xShift, (j * yOffset) + yShift] and
                    pix[(i * xOffset) + xShift, (j * yOffset) + yShift] != self.gopix2[(i * xOffset) + xShift, (j * yOffset) + yShift] and
                    pix[(i * xOffset) + xShift, (j * yOffset) + yShift] != self.gopix3[(i * xOffset) + xShift, (j * yOffset) + yShift]):
                    return False

        return True
