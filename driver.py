# Gideon Marsh
# github.com/GideonMarsh

import screenshotter
import fitness
from math import floor
from time import time, sleep
from pynput.keyboard import Key, Controller


windowName='Mega Man Legacy Collection'
keyboard = Controller()

# screenRatio = 1.333
xPixels = 266
yPixels = 200

# initial setup
screenshotter.setWindowSize(windowName)
sleep(3)
region = screenshotter.findBounds(windowName)
if (region[3] < yPixels or region[2] < xPixels):
    print('Screen not large enough')
'''
startTime = time()
pressflag = True
releaseflag = True
'''
#runTimer = fitness.RunTimer(1)

# program loop
print('time started')
#runTimer.startTimer()
while (not screenshotter.isProgramOver(windowName)):
    startTime = time()
    '''
    if (time() > startTime + 2 and pressflag):
        print('press')
        keyboard.press(Key.right)
        pressflag = False
    if (time() > startTime + 4 and releaseflag):
        keyboard.release(Key.right)
        print('release')
        releaseflag = False
    '''
    screenshot = screenshotter.takescreenshot(windowName, region)
    if (screenshot):
        grayimg = screenshot.convert('L')
        pix = grayimg.load()

        yOffset = floor(grayimg.height / yPixels)
        xOffset = floor(grayimg.width / xPixels)
        xShift = floor((grayimg.width % xPixels) / 2)
        yShift = floor((grayimg.height % yPixels) / 2)

        for i in range(xPixels):
            for j in range(yPixels):
                pix[i,j] = pix[(i * xOffset) + xShift, (j * yOffset) + yShift]

    #print(grayimg.width)
    #print(grayimg.height)

    #grayimg.save('testscreenshot.png')
    '''
    if (runTimer.isTimeUp()):
        print('Time Over!')
    else:
        print('still going...')
    '''
    print(time() - startTime)

# safe shut down
#runTimer.cancelTimer()
