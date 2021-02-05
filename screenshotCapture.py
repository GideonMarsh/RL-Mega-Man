# Gideon Marsh
# github.com/GideonMarsh

import screenshotter
import controller
import constants
from time import sleep
from pynput.keyboard import Key, Listener

'''
A driver program for capturing screenshots
'''

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
        grayimg.save('images/early_out_airman.png')

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
