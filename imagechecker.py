# Gideon Marsh
# github.com/GideonMarsh

import constants
from PIL import Image
from math import floor
import numpy as np
import scipy.signal

# this method is from https://stackoverflow.com/questions/24768222/how-to-detect-a-shift-between-images
def cross_image(im1, im2):
   # get rid of the color channels by performing a grayscale transform
   # the type cast into 'float' is to avoid overflows
   im1_gray = np.sum(im1.astype('float'), axis=2)
   im2_gray = np.sum(im2.astype('float'), axis=2)

   # get rid of the averages, otherwise the results are not good
   im1_gray -= np.mean(im1_gray)
   im2_gray -= np.mean(im2_gray)

   # calculate the correlation image; note the flipping of onw of the images
   return scipy.signal.fftconvolve(im1_gray, im2_gray[::-1,::-1], mode='same')

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

    def checkScreenTranslation(self, newScreen):
        try:
            oldScreen = Image.open('images/lastScreenshot.png')

            npix = newScreen.load()
            opix = oldScreen.load()

            w = (constants.XPIXELS * 2)
            h = (constants.YPIXELS * 2)

            xOffset = floor(oldScreen.width / w)
            yOffset = floor(oldScreen.height / h)
            xShift = floor((oldScreen.width % w) / 2)
            yShift = floor((oldScreen.height % h) / 2)

            newpix = list()
            oldpix = list()
            for j in range(h):
                newlist = list()
                oldlist = list()
                for i in range(w):
                    newlist.append(npix[(i * xOffset) + xShift,(j * yOffset) + yShift])
                    oldlist.append(opix[(i * xOffset) + xShift,(j * yOffset) + yShift])
                newpix.append(newlist)
                oldpix.append(oldlist)

            newArray = np.array(newpix, dtype=np.uint8)
            oldArray = np.array(oldpix, dtype=np.uint8)

            corr_img = cross_image(newArray, oldArray)
            coords = np.unravel_index(np.argmax(corr_img), corr_img.shape)

            translation = coords[1] - (w / 2)

            if (translation <= 10 and translation >= -10):
                newScreen.save('images/lastScreenshot.png')
                return translation
            return 0

        except FileNotFoundError:
            newScreen.save('images/lastScreenshot.png')
            return 0
'''
def checkPixelLoops(p, cp, xo, yo, xs, ys, xp, yp):
    for i in range(xp):
        for j in range(yp):
            if (p[(i * xo) + xs, (j * yo) + ys] != cp[(i * xo) + xs, (j * yo) + ys]):
                return False
    return True
'''
