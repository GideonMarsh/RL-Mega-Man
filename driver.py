# Gideon Marsh
# github.com/GideonMarsh

import constants
import imagechecker
import screenshotter
import fitness
import controller
from time import time, sleep

from pynput.keyboard import Key, Listener

##################### Keyboard listener functions #######################

grayimg = None

def on_press(key):
    '''
    print('{0} pressed'.format(
        key))
    '''
    if (key == Key.space):
        grayimg.save('images/checkpoint_air_man_1.png')

def on_release(key):
    '''
    print('{0} release'.format(key))
    if key == Key.esc:
        # Stop listener
        return False
    '''

############################# initial setup #############################
'''
Manual steps to take before running program:
1. Make sure all checkpoint images are saved and ready for comparison
2. Save the game at the start of the level that is being played immediately after the word 'READY' stops appearing
3. Navigate to a menu without a black background (stage select works)
4. Open options menu
5. Start program
'''
screenshotter.setWindowSize(constants.WINDOWNAME)
sleep(0.2)
controller.closeMenu()
sleep(0.1)
region = screenshotter.findBounds(constants.WINDOWNAME)
if (region[3] < constants.YPIXELS or region[2] < constants.XPIXELS):
    print('Screen not large enough')
else:
    print('Screen region acquired')

fitnessTracker = fitness.FitnessTimer()

imageCheck = imagechecker.ImageChecker()
imageCheck.imageSetup()

runcounter = 1

keyListener = Listener(on_press=on_press,on_release=on_release)
keyListener.start()

globalTimer = fitness.RunTimer(constants.TOTAL_TIMEOUT)

############################# program loop ##############################
controller.loadSave()
fitnessTracker.setStartTime()
while (not screenshotter.isProgramOver(constants.WINDOWNAME)):
    screenshot = screenshotter.takescreenshot(constants.WINDOWNAME, region)
    if (screenshot):
        grayimg = screenshot.convert('L')

        ################### Checks for end of run ###################

        # program gets a game over
        if (imageCheck.checkGameOver(grayimg,constants.XPIXELS,constants.YPIXELS) != 0):
            fitnessTracker.setEndTime()
            # calculate and set fitness here
            fit = fitnessTracker.getFitness()
            print('Fitness for run ' + str(runcounter) + ': ' + str(fit))
            runcounter = runcounter + 1
            fitnessTracker.setStartTime()
            controller.loadSave()

        # program completes the level
        if (imageCheck.checkLevelComplete(grayimg, constants.XPIXELS,constants.YPIXELS)):
            fitnessTracker.setEndTime()
            # calculate, award, and set fitness here
            fit = (constants.SECTION_TIMEOUT * 2) - fitnessTracker.getFitness()
            print('Fitness for run ' + str(runcounter) + ': ' + str(fit))
            runcounter = runcounter + 1
            fitnessTracker.setStartTime()
            controller.loadSave()

        # program stops changing inputs

        # program stops making progress

        # program times out


############################ safe shut down #############################
keyListener.stop()
