# Gideon Marsh
# github.com/GideonMarsh

import screenshotter
import controller
import constants
from time import sleep
from pynput.keyboard import Key, Listener
from math import floor

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

def on_press(key):
    '''
    print('{0} pressed'.format(key))
    '''
    if (key == Key.space):

        pix = grayimg.load()

        xShift = 120
        ycoords = [68,75,83,91,98,107,114,122,130,137,145,152,160,168,176,183,191,198,205,214,222,229,237,245,253,260,268,275]

        for i in range(20):
            for j in range(28):
                pix[i + 140,ycoords[j]] = pix[i + xShift,ycoords[j]]

        hp = 0
        for c in ycoords:
            if pix[120,c] > 5:
                hp = hp + 1

        print(hp)

        grayimg.save(screenshotName)

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
        grayimg = screenshot.convert('L')
keyListener.stop()
