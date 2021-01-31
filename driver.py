# Gideon Marsh
# github.com/GideonMarsh

import constants
import imagechecker
import screenshotter
import fitness
import controller
from time import time, sleep

############################# initial setup #############################
'''
Manual steps to take before running program:
1. Make sure all checkpoint images are saved and ready for comparison
2. Save the game at the start of the level that is being played with only one life remaining
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

runcounter = 1

############################# program loop ##############################
controller.loadSave()
fitnessTracker.setStartTime()
while (not screenshotter.isProgramOver(constants.WINDOWNAME)):
    screenshot = screenshotter.takescreenshot(constants.WINDOWNAME, region)
    if (screenshot):
        grayimg = screenshot.convert('L')

        if (imagechecker.checkGameOver(grayimg,constants.XPIXELS,constants.YPIXELS)):
            fitnessTracker.setEndTime()
            print('Fitness for run ' + str(runcounter) + ': ' + str(fitnessTracker.getFitness()))
            runcounter = runcounter + 1
            controller.loadSave()

############################# safe shut down ############################
