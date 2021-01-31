# Gideon Marsh
# github.com/GideonMarsh

import imagechecker
import screenshotter
import fitness
from time import time, sleep
from pynput.keyboard import Key, Controller

# screenRatio = 1.333
xPixels = 266
yPixels = 200

windowName='Mega Man Legacy Collection'
keyboard = Controller()

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
#runTimer.startTimer()
grayimg = None
while (not screenshotter.isProgramOver(windowName)):
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

        if (imagechecker.checkGameOver(grayimg,xPixels,yPixels)):
            print('Game Over!')


    '''
    #print(grayimg.width)
    #print(grayimg.height)

    #grayimg.save('testscreenshot.png')
    if (runTimer.isTimeUp()):
        print('Time Over!')
    else:
        print('still going...')
    '''

# safe shut down
#runTimer.cancelTimer()
