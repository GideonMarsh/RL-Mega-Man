# Gideon Marsh
# github.com/GideonMarsh

import ga
import constants
import imagechecker
import screenshotter
import fitness
import controller
from time import time, sleep

from pynput.keyboard import Key, Listener
'''
NOTE:
Keyboard listener will pick up user keyboard inputs
It will NOT pick up controller inputs
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
currentlyPlaying = False
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

fitnessTracker = fitness.FitnessTimer()

imageCheck = imagechecker.ImageChecker()
imageCheck.imageSetup()

runcounter = 0

globalTimer = fitness.RunTimer(constants.TOTAL_TIMEOUT)
inputTimer = fitness.RunTimer(constants.CONTROL_TIMEOUT)
progressCheckTimer = fitness.RunTimer(constants.PROGRESS_CHECK_WAIT_INTERVAL)
checkProgress = False

grayimg = None

firstImageTaken = False

brains = ga.GeneticAlgorithmController(constants.POPULATION_SIZE, constants.MUTATION_CHANCE, 100)

### helper functions rely on above variables ###

def on_press(key):
    '''
    print('{0} pressed'.format(
        key))
    '''
    if (key == Key.space):
        grayimg.save('images/last_checkpoint.png')
    if (currentlyPlaying):
        global inputTimer
        inputTimer.cancelTimer()
        inputTimer = fitness.RunTimer(constants.CONTROL_TIMEOUT)
        inputTimer.startTimer()

def on_release(key):
    '''
    print('{0} release'.format(key))
    if key == Key.esc:
        # Stop listener
        return False
    '''
    if (currentlyPlaying):
        global inputTimer
        inputTimer.cancelTimer()
        inputTimer = fitness.RunTimer(constants.CONTROL_TIMEOUT)
        inputTimer.startTimer()

# call this function before the start of every run
def restartRun():
    global globalTimer, runcounter, inputTimer, currentlyPlaying, progressCheckTimer, checkProgress
    inputTimer.cancelTimer()
    globalTimer.cancelTimer()
    progressCheckTimer.cancelTimer()
    inputTimer = fitness.RunTimer(constants.CONTROL_TIMEOUT)
    globalTimer = fitness.RunTimer(constants.TOTAL_TIMEOUT)
    progressCheckTimer = fitness.RunTimer(constants.PROGRESS_CHECK_WAIT_INTERVAL)
    runcounter = runcounter + 1
    controller.loadSave()
    fitnessTracker.setStartTime()
    globalTimer.startTimer()
    inputTimer.startTimer()
    progressCheckTimer.startTimer()
    checkProgress = False
    firstImageTaken = False
    currentlyPlaying = True

# call this whenever a run completes
def endRun():
    global currentlyPlaying
    currentlyPlaying = False
    controller.cutoffInputs()
    controller.openMenu()
    fitnessTracker.setEndTime()

### remaining variable setup relies on above helper functions ###x
keyListener = Listener(on_press=on_press,on_release=on_release)
keyListener.start()

############################# program loop ##############################
restartRun()
while (not screenshotter.isProgramOver(constants.WINDOWNAME)):
    #print(fitnessTracker.getFitness())
    screenshot = screenshotter.takescreenshot(constants.WINDOWNAME, region)
    if (screenshot):
        grayimg = screenshot.convert('L')

        controller.changeInputs(brains.passInputs(grayimg))

        if (not firstImageTaken):
            grayimg.save('images/last_checkpoint.png')
            firstImageTaken = True

        if (progressCheckTimer.timeUp()):
            if (checkProgress):
                print('waiting')
                progressCheckTimer.cancelTimer()
                checkProgress = False
                grayimg.save('images/last_checkpoint.png')
                progressCheckTimer = fitness.RunTimer(constants.PROGRESS_CHECK_WAIT_INTERVAL)
                progressCheckTimer.startTimer()
            else:
                print('checking progress')
                progressCheckTimer.cancelTimer()
                checkProgress = True
                progressCheckTimer = fitness.RunTimer(constants.PROGRESS_CHECK_COMPARE_INTERVAL)
                progressCheckTimer.startTimer()

        ################### Checks for end of run ###################

        # program gets a game over
        if (imageCheck.checkGameOver(grayimg)):
            endRun()
            fit = fitnessTracker.getFitness()
            brains.assignFitness(fit)
            print('Fitness for run ' + str(runcounter) + ': ' + str(fit))
            restartRun()

        # program completes the level
        if (imageCheck.checkLevelComplete(grayimg)):
            endRun()
            fit = (constants.TOTAL_TIMEOUT * 2) - fitnessTracker.getFitness()
            brains.assignFitness(fit)
            print('Fitness for run ' + str(runcounter) + ': ' + str(fit))
            restartRun()

        # program stops changing inputs
        if (inputTimer.timeUp()):
            endRun()
            fit = fitnessTracker.getFitness() - constants.CONTROL_TIMEOUT
            brains.assignFitness(fit)
            print('Fitness for run ' + str(runcounter) + ': ' + str(fit))
            restartRun()

        # program stops making progress
        if (checkProgress and imageCheck.checkNoProgress(grayimg)):
            endRun()
            fit = fitnessTracker.getFitness() - constants.PROGRESS_CHECK_WAIT_INTERVAL
            brains.assignFitness(fit)
            print('Fitness for run ' + str(runcounter) + ': ' + str(fit))
            restartRun()

        # program times out
        if (globalTimer.timeUp()):
            endRun()
            fit = 0
            brains.assignFitness(fit)
            print('Fitness for run ' + str(runcounter) + ': ' + str(fit))
            restartRun()


############################ safe shut down #############################
controller.cutoffInputs()
keyListener.stop()
globalTimer.cancelTimer()
inputTimer.cancelTimer()
progressCheckTimer.cancelTimer()
