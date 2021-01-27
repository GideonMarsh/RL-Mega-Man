# Gideon Marsh
# github.com/GideonMarsh

import screenshotter
import math
import time


windowName='Mega Man Legacy Collection'

# screenRatio = 1.333
xPixels = 266
yPixels = 200

screenshotter.setWindowSize(windowName)
time.sleep(3)
#while True:
region = screenshotter.findBounds(windowName)
if (region[3] < yPixels or region[2] < xPixels):
    print('Screen not large enough')
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

    #for i in range(math.floor(grayimg.width)):
    #    for j in range(math.floor(grayimg.height)):
    print(grayimg.width)
    print(grayimg.height)


    grayimg.save('testscreenshot.png')
