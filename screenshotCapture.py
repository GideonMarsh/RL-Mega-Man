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
import cv2

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

imagecount = 0

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
    global imagecount
    '''
    print('{0} pressed'.format(key))
    '''

    if (key == Key.space):
        '''
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
        '''

        #screenshot.save(screenshotName)
        screenshot.save('images/stitchtest_' + str(imagecount) + '.png')
        imagecount += 1


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
counter = 0
while (continueGame and not screenshotter.isProgramOver(constants.WINDOWNAME)):
    screenshot = screenshotter.takescreenshot(constants.WINDOWNAME, region)
    if (screenshot):

        if counter == 20:
            screenshot.save('images/stitchtest_' + str(imagecount) + '.png')
            imagecount += 1
            counter = 0
        else:
            counter += 1
        '''
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
        '''
keyListener.stop()

images = list()
for i in range(imagecount):
    images.append(cv2.imread('images/stitchtest_' + str(i) + '.png'))

stitcher = cv2.Stitcher_create()
(status, stitched) = stitcher.stitch(images, cv2.Stitcher_PANORAMA)
print(status)
cv2.imwrite('images/stitched.png', stitched)
