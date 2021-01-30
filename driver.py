# Gideon Marsh
# github.com/GideonMarsh

import screenshotter
import math
import time
from pynput.keyboard import Key, Controller


windowName='Mega Man Legacy Collection'
keyboard = Controller()

# screenRatio = 1.333
xPixels = 266
yPixels = 200

# initial setup
screenshotter.setWindowSize(windowName)
time.sleep(3)
region = screenshotter.findBounds(windowName)
if (region[3] < yPixels or region[2] < xPixels):
    print('Screen not large enough')
'''
startTime = time.time()
pressflag = True
releaseflag = True
'''

# program loop
while (not screenshotter.isProgramOver(windowName)):
    '''
    if (time.time() > startTime + 2 and pressflag):
        print('press')
        keyboard.press(Key.right)
        pressflag = False
    if (time.time() > startTime + 4 and releaseflag):
        keyboard.release(Key.right)
        print('release')
        releaseflag = False
    '''
    screenshot = screenshotter.takescreenshot(windowName, region)
    if (screenshot):
        grayimg = screenshot.convert('L')
        pix = grayimg.load()

        yOffset = math.floor(grayimg.height / yPixels)
        xOffset = math.floor(grayimg.width / xPixels)
        xShift = math.floor((grayimg.width % xPixels) / 2)
        yShift = math.floor((grayimg.height % yPixels) / 2)

        for i in range(xPixels):
            for j in range(yPixels):
                pix[i,j] = pix[(i * xOffset) + xShift, (j * yOffset) + yShift]

    #print(grayimg.width)
    #print(grayimg.height)

    #grayimg.save('testscreenshot.png')

# safe shut down
