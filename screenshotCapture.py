# Gideon Marsh
# github.com/GideonMarsh

import screenshotter
import controller
import constants
from time import sleep
from pynput.keyboard import Key, Listener
from math import floor
import numpy as np
import scipy.signal
from PIL import Image

'''
A driver program for capturing screenshots

Start the program the same way as the main driver
Make sure the name of the screenshot you want to capture is correct
Press spacebar to capture the screenshot
Press 'w' or leave the window to end the program
'''

screenshotName = 'images/sizetest.png'
xp = 60
yp = 45

screenshotter.setWindowSize(constants.WINDOWNAME)
controller.cutoffInputs()
sleep(0.2)
controller.closeMenu()
sleep(0.1)
region = screenshotter.findBounds(constants.WINDOWNAME)
if (region[3] < constants.YPIXELS or region[2] < constants.XPIXELS):
    print('Screen not large enough')
else:
    print('Screen region acquired')
controller.openMenu()

grayimg = None

continueGame = True

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

def on_press(key):
    '''
    print('{0} pressed'.format(key))
    '''
    if (key == Key.space):

        pix = screenshot.load()

        xOffset = floor(screenshot.width / (constants.XPIXELS*2))
        yOffset = floor(screenshot.height / (constants.YPIXELS*2))
        xShift = floor((screenshot.width % (constants.XPIXELS*2)) / 2)
        yShift = floor((screenshot.height % (constants.YPIXELS*2)) / 2)

        newpix = list()
        for j in range(constants.YPIXELS*2):
            newlist = list()
            for i in range(constants.XPIXELS*2):
                newlist.append(pix[(i * xOffset) + xShift,(j * yOffset) + yShift])
            newpix.append(newlist)

        # Convert the pixels into an array using numpy
        array = np.array(newpix, dtype=np.uint8)

        # Use PIL to create an image from the new array of pixels
        new_image = Image.fromarray(array)
        new_image.save('images/new.png')


        #screenshot.save(screenshotName)


def on_release(key):
    '''
    print('{0} release'.format(key))
    if key == Key.esc:
        # Stop listener
        return False
    '''
    try:
        if (key.char == 'w'):
            global continueGame
            continueGame = False
    except AttributeError:
        pass

keyListener = Listener(on_press=on_press,on_release=on_release)
keyListener.start()

controller.loadSave()
while (continueGame and not screenshotter.isProgramOver(constants.WINDOWNAME)):
    screenshot = screenshotter.takescreenshot(constants.WINDOWNAME, region)
    if (screenshot):
        #grayimg = screenshot.convert('L')

        pix = screenshot.load()

        xOffset = floor(screenshot.width / (constants.XPIXELS*2))
        yOffset = floor(screenshot.height / (constants.YPIXELS*2))
        xShift = floor((screenshot.width % (constants.XPIXELS*2)) / 2)
        yShift = floor((screenshot.height % (constants.YPIXELS*2)) / 2)

        newpix = list()
        for j in range(constants.YPIXELS*2):
            newlist = list()
            for i in range(constants.XPIXELS*2):
                newlist.append(pix[(i * xOffset) + xShift,(j * yOffset) + yShift])
            newpix.append(newlist)

        # Convert the pixels into an array using numpy
        array = np.array(newpix, dtype=np.uint8)
        image = Image.open('images/new.png')
        data = np.asarray(image)
        corr_img = cross_image(array, data)
        print(np.unravel_index(np.argmax(corr_img), corr_img.shape))
keyListener.stop()
