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
4. Open options menu (cursor should be on 'SAVE GAME')
5. Start program

Press 'w' to end the program safely
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

continueGame = True

globalTimer = fitness.RunTimer(constants.TOTAL_TIMEOUT)
progressCheckTimer = fitness.RunTimer(constants.PROGRESS_CHECK_EARLY_TIMEOUT)
controlTimer = fitness.RunTimer(constants.CONTROL_TIMEOUT)
checkProgress = False

grayimg = None

firstImageTaken = False

brains = ga.GeneticAlgorithmController(constants.POPULATION_SIZE, 15, constants.MUTATION_CHANCE)

### helper functions rely on above variables ###

def on_press(key):
    '''
    print('{0} pressed'.format(key))
    if (key == Key.space):
        grayimg.save('images/last_checkpoint.png')
    '''

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

# call this function before the start of every run
def restartRun():
    global globalTimer, currentlyPlaying, progressCheckTimer, checkProgress, firstImageTaken, controlTimer
    globalTimer.cancelTimer()
    progressCheckTimer.cancelTimer()
    controlTimer.cancelTimer()
    globalTimer = fitness.RunTimer(constants.TOTAL_TIMEOUT)
    progressCheckTimer = fitness.RunTimer(constants.PROGRESS_CHECK_EARLY_TIMEOUT)
    controlTimer = fitness.RunTimer(constants.CONTROL_TIMEOUT)

    if (brains.doneWithGeneration()):
        brains.makeNextGeneration()
    print('Generation ' + str(brains.getIndividualInfo()[0]) + '; Player ' + str(brains.getIndividualInfo()[1]))

    controller.resetInputMemory()
    controller.loadSave()
    fitnessTracker.setStartTime()
    globalTimer.startTimer()
    progressCheckTimer.startTimer()
    controlTimer.startTimer()
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

### remaining variable setup relies on above helper functions ###
keyListener = Listener(on_press=on_press,on_release=on_release)
keyListener.start()

############################# program loop ##############################
restartRun()
while (continueGame and not screenshotter.isProgramOver(constants.WINDOWNAME)):
    #print(fitnessTracker.getFitness())
    screenshot = screenshotter.takescreenshot(constants.WINDOWNAME, region)
    if (screenshot):
        grayimg = screenshot.convert('L')

        if controller.changeInputs(brains.passInputs(grayimg)):
            #print('control timer restart')
            grayimg.save('images/control_checkpoint.png')
            controlTimer.cancelTimer()
            controlTimer = fitness.RunTimer(constants.CONTROL_TIMEOUT)
            controlTimer.startTimer()


        if (not firstImageTaken):
            grayimg.save('images/last_checkpoint.png')
            firstImageTaken = True

        if (progressCheckTimer.timeUp()):
            if (checkProgress):
                progressCheckTimer.cancelTimer()
                checkProgress = False
                grayimg.save('images/last_checkpoint.png')
                progressCheckTimer = fitness.RunTimer(constants.PROGRESS_CHECK_TIMEOUT)
                progressCheckTimer.startTimer()
            else:
                progressCheckTimer.cancelTimer()
                checkProgress = True
                progressCheckTimer = fitness.RunTimer(constants.PROGRESS_CHECK_COMPARE_INTERVAL)
                progressCheckTimer.startTimer()

        ################### Checks for end of run ###################

        # program gets a game over
        if (imageCheck.checkGameOver(grayimg)):
            endRun()
            # subtract the number of seconds the game over effect takes
            fit = fitnessTracker.getFitness()
            brains.assignFitness(fit)
            print('Fitness: ' + str(fit) + ' (game over)')
            restartRun()

        # program completes the level
        if (imageCheck.checkLevelComplete(grayimg)):
            endRun()
            fit = (constants.TOTAL_TIMEOUT * 2) - fitnessTracker.getFitness()
            brains.assignFitness(fit)
            print('Fitness: ' + str(fit) + ' (level complete)')
            restartRun()

        # program stops making progress
        if (checkProgress and imageCheck.checkNoProgress(grayimg)):
            endRun()
            fit = fitnessTracker.getFitness() - constants.PROGRESS_CHECK_TIMEOUT
            if (fit < 0):
                fit = 0
            if (imageCheck.checkEarlyOut(grayimg)):
                fit = 0
            brains.assignFitness(fit)
            print('Fitness: ' + str(fit) + ' (no progress)')
            restartRun()

        # program stops controlling character
        if (controlTimer.timeUp() and imageCheck.checkNoControl(grayimg)):
            endRun()
            fit = fitnessTracker.getFitness() - constants.CONTROL_TIMEOUT
            if (imageCheck.checkEarlyOut(grayimg)):
                fit = 0
            brains.assignFitness(fit)
            print('Fitness: ' + str(fit) + ' (no control)')
            restartRun()

        # program times out
        if (globalTimer.timeUp()):
            endRun()
            fit = 0
            brains.assignFitness(fit)
            print('Fitness: ' + str(fit) + ' (time out)')
            restartRun()


############################ safe shut down #############################
controller.cutoffInputs()
keyListener.stop()
globalTimer.cancelTimer()
progressCheckTimer.cancelTimer()
controlTimer.cancelTimer()
