# Gideon Marsh
# github.com/GideonMarsh

import constants
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
        self.eopix  = Image.open('images/early_out_air_man.png').load()

    # check if the incoming image exactly matches any of the game over images
    def checkGameOver(self, image):
        pix = image.load()

        xOffset = floor(image.width / constants.XPIXELS)
        yOffset = floor(image.height / constants.YPIXELS)
        xShift = floor((image.width % constants.XPIXELS) / 2)
        yShift = floor((image.height % constants.YPIXELS) / 2)

        for i in range(constants.XPIXELS):
            for j in range(constants.YPIXELS):
                if (pix[(i * xOffset) + xShift, (j * yOffset) + yShift] != self.gopix1[(i * xOffset) + xShift, (j * yOffset) + yShift] and
                    pix[(i * xOffset) + xShift, (j * yOffset) + yShift] != self.gopix2[(i * xOffset) + xShift, (j * yOffset) + yShift] and
                    pix[(i * xOffset) + xShift, (j * yOffset) + yShift] != self.gopix3[(i * xOffset) + xShift, (j * yOffset) + yShift]):
                    return False

        return True

    # check if the incoming image exactly matches the level complete image
    def checkLevelComplete(self, image):
        pix = image.load()

        xOffset = floor(image.width / constants.XPIXELS)
        yOffset = floor(image.height / constants.YPIXELS)
        xShift = floor((image.width % constants.XPIXELS) / 2)
        yShift = floor((image.height % constants.YPIXELS) / 2)

        for i in range(constants.XPIXELS):
            for j in range(constants.YPIXELS):
                if (pix[(i * xOffset) + xShift, (j * yOffset) + yShift] != self.winpix[(i * xOffset) + xShift, (j * yOffset) + yShift]):
                    return False

        return True

    # check if the incoming image closely matches the last checkpoint image
    def checkNoProgress(self, image):
        try:
            check = Image.open('images/last_checkpoint.png')

            pix = image.load()

            checkpix = check.load()

            xOffset = floor(image.width / constants.XPIXELS)
            yOffset = floor(image.height / constants.YPIXELS)
            xShift = floor((image.width % constants.XPIXELS) / 2)
            yShift = floor((image.height % constants.YPIXELS) / 2)

            errorMargin = round(constants.XPIXELS * constants.YPIXELS * constants.IMAGE_ACCEPTABLE_ERROR)
            errorCount = 0

            for i in range(constants.XPIXELS):
                for j in range(constants.YPIXELS):
                    if (pix[(i * xOffset) + xShift, (j * yOffset) + yShift] != checkpix[(i * xOffset) + xShift, (j * yOffset) + yShift]):
                        errorCount = errorCount + 1
                    if (errorCount >= errorMargin):
                        return False

            return True
        except FileNotFoundError:
            return False

    # check if the incoming image closely matches the control checkpoint image
    def checkNoControl(self, image):
        try:
            check = Image.open('images/control_checkpoint.png')

            pix = image.load()

            checkpix = check.load()

            xOffset = floor(image.width / constants.XPIXELS)
            yOffset = floor(image.height / constants.YPIXELS)
            xShift = floor((image.width % constants.XPIXELS) / 2)
            yShift = floor((image.height % constants.YPIXELS) / 2)

            errorMargin = round(constants.XPIXELS * constants.YPIXELS * constants.IMAGE_ACCEPTABLE_ERROR)
            errorCount = 0

            for i in range(constants.XPIXELS):
                for j in range(constants.YPIXELS):
                    if (pix[(i * xOffset) + xShift, (j * yOffset) + yShift] != checkpix[(i * xOffset) + xShift, (j * yOffset) + yShift]):
                        errorCount = errorCount + 1
                    if (errorCount >= errorMargin):
                        return False

            return True
        except FileNotFoundError:
            return False

    # check if the incoming image loosely matches the early out image, if any
    def checkEarlyOut(self, image):
        try:
            if not self.eopix:
                raise FileNotFoundError()

            pix = image.load()

            xOffset = floor(image.width / constants.XPIXELS)
            yOffset = floor(image.height / constants.YPIXELS)
            xShift = floor((image.width % constants.XPIXELS) / 2)
            yShift = floor((image.height % constants.YPIXELS) / 2)

            errorMargin = round(constants.XPIXELS * constants.YPIXELS * constants.IMAGE_ACCEPTABLE_ERROR * 4)
            errorCount = 0

            for i in range(constants.XPIXELS):
                for j in range(constants.YPIXELS):
                    if (pix[(i * xOffset) + xShift, (j * yOffset) + yShift] != self.eopix[(i * xOffset) + xShift, (j * yOffset) + yShift]):
                        errorCount = errorCount + 1
                    if (errorCount >= errorMargin):
                        return False

            return True
        except FileNotFoundError:
            return False

    def checkHP(self, image):
        pix = image.load()

        xShift = 120
        ycoords = [68,75,83,91,98,107,114,122,130,137,145,152,160,168,176,183,191,198,205,214,222,229,237,245,253,260,268,275]

        hp = 28
        for c in ycoords:
            if pix[xShift,c] < 5:
                hp = hp - 1
            else:
                break
        
        return hp
'''
def checkPixelLoops(p, cp, xo, yo, xs, ys, xp, yp):
    for i in range(xp):
        for j in range(yp):
            if (p[(i * xo) + xs, (j * yo) + ys] != cp[(i * xo) + xs, (j * yo) + ys]):
                return False
    return True
'''
