# Gideon Marsh
# github.com/GideonMarsh

import ga
import brain
import constants
import imagechecker
import screenshotter
import fitness
import controller
from time import time, sleep
from datetime import datetime, timedelta
import pickle
from os import path
import log

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
2. Save the game at the start of the level that is being played immediately after Mega Man becomes controllable
3. Navigate to a menu without a black background (stage select works)
4. Open options menu (cursor should be on 'SAVE GAME')
5. Start program

Press 'w' to save progress and end the program safely
Press 't' to end without saving progress
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
# penalties are applied in order of subtraction then multiplicationthat order
fitnessPenaltySub = 0
fitnessPenaltyMult = 1

imageCheck = imagechecker.ImageChecker()
imageCheck.imageSetup()

continueGame = True
saveProgress = True

globalTimer = fitness.RunTimer(constants.TOTAL_TIMEOUT)
progressCheckTimer = fitness.RunTimer(constants.PROGRESS_CHECK_EARLY_TIMEOUT)
controlTimer = fitness.RunTimer(constants.CONTROL_TIMEOUT)
controlImageTimer = fitness.RunTimer(2)
checkProgress = False

grayimg = None

firstImageTaken = False
controlImageTaken = False

runNumber = 1

# check if saved population exists and load it
# if none exists, create new population from the beginning
brains = None
if path.exists(constants.SAVE_FILE_NAME):
    with open(constants.SAVE_FILE_NAME, 'rb') as input:
        brains = pickle.load(input)
        c = pickle.load(input)
        brain.nodeCount = c[0]
        brain.connectionCount = c[1]
        ga.speciesCounter = c[2]
        print('Population loaded')
else:
    brains = ga.GeneticAlgorithmController(constants.POPULATION_SIZE, 25)
    print('No saved population found - creating population from scratch')

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
        global continueGame, saveProgress
        if (key.char == 'w'):
            continueGame = False
        if (key.char == 't'):
            continueGame = False
            saveProgress = False
    except AttributeError:
        pass

# call this function before the start of every run
def restartRun():
    global globalTimer, currentlyPlaying, progressCheckTimer, checkProgress, firstImageTaken, controlTimer, controlImageTimer, controlImageTaken, fitnessPenaltySub, fitnessPenaltyMult, nextTick, runNumber, newFitness
    globalTimer.cancelTimer()
    progressCheckTimer.cancelTimer()
    controlTimer.cancelTimer()
    controlImageTimer.cancelTimer()
    globalTimer = fitness.RunTimer(constants.TOTAL_TIMEOUT)
    progressCheckTimer = fitness.RunTimer(constants.PROGRESS_CHECK_EARLY_TIMEOUT)
    controlTimer = fitness.RunTimer(constants.CONTROL_TIMEOUT)
    controlImageTimer = fitness.RunTimer(2)
    fitnessPenaltySub = 0
    fitnessPenaltyMult = 1
    newFitness = 0

    if (brains.doneWithGeneration()):
        if (runNumber == 1):
            runNumber = 1
            brains.setBestBrain()
            log.writeToLog(brains)
            f = constants.SAVE_FOLDER + 'Generation_' + str(brains.generation) + '.pkl'
            with open(f, 'wb') as output:
                pickle.dump(brains, output, pickle.HIGHEST_PROTOCOL)
                c = [brain.nodeCount, brain.connectionCount, ga.speciesCounter]
                pickle.dump(c,output,pickle.HIGHEST_PROTOCOL)
                print('Generation ' + str(brains.generation) + ' saved')
            brains.makeNextGeneration()
            with open(constants.SAVE_FILE_NAME, 'wb') as output:
                pickle.dump(brains, output, pickle.HIGHEST_PROTOCOL)
                c = [brain.nodeCount, brain.connectionCount, ga.speciesCounter]
                pickle.dump(c,output,pickle.HIGHEST_PROTOCOL)
                print('Population saved')
        else:
            runNumber = runNumber + 1
            brains.currentBrain = 0

    print('Generation ' + str(brains.getIndividualInfo()[0]) + '; Species ' + str(brains.getIndividualInfo()[1]) + '; Player ' + str(brains.getIndividualInfo()[2]) + '; Run ' + str(runNumber))
    if (brains.getIndividualInfo()[1] == -1):
        raise AttributeError('-1 is not a species')

    controller.resetInputMemory()
    controller.loadSave()
    fitnessTracker.setStartTime()
    globalTimer.startTimer()
    progressCheckTimer.startTimer()
    controlTimer.startTimer()
    controlImageTimer.startTimer()
    checkProgress = False
    firstImageTaken = False
    controlImageTaken = False
    currentlyPlaying = True
    '''
    now = datetime.now()
    if now.microsecond >= 100000:
        nextTick = now.replace(microsecond=100000) + timedelta(microseconds=100000)
    else:
        nextTick = now.replace(microsecond=0) + timedelta(microseconds=100000)
    '''
    nextTick = datetime.now() + timedelta(microseconds=100000)

# call this whenever a run completes
def endRun():
    global currentlyPlaying, newFitness
    #print('Fitness: ' + str(newFitness))
    currentlyPlaying = False
    controller.cutoffInputs()
    controller.openMenu()
    fitnessTracker.setEndTime()

### remaining variable setup relies on above helper functions ###
keyListener = Listener(on_press=on_press,on_release=on_release)
keyListener.start()

############################# program loop ##############################
try:
    restartRun()
    timeList = list()
    while (continueGame and not screenshotter.isProgramOver(constants.WINDOWNAME)):
        # wait for the next tick
        while (datetime.now() < nextTick):
            pass
        screenshot = screenshotter.takescreenshot(constants.WINDOWNAME, region)

        '''
        now = datetime.now().microsecond
        print(str(now) + ' ' + str(nextTick))
        timeList.append(now % 100000)
        '''

        if (screenshot):
            grayimg = screenshot.convert('L')

            newHPmod = (imageCheck.checkHP(grayimg) + 2) / 30
            fitnessPenaltyMult = min(fitnessPenaltyMult,newHPmod)

            if controller.changeInputs(brains.passInputs(grayimg)):
                fitnessPenaltySub = fitnessPenaltySub + constants.CONTROL_FITNESS_PENALTY
                #print('control timer restart')
                controlTimer.cancelTimer()
                controlTimer = fitness.RunTimer(constants.CONTROL_TIMEOUT)
                controlTimer.startTimer()

                controlImageTimer.cancelTimer()
                controlImageTimer = fitness.RunTimer(2)
                controlImageTimer.startTimer()
                controlImageTaken = False

            if (controlImageTimer.timeUp() and not controlImageTaken):
                grayimg.save('images/control_checkpoint.png')
                controlImageTaken = True
                #print('control image taken')

            if (not firstImageTaken):
                grayimg.save('images/last_checkpoint.png')
                imageCheck.saveNewImage(screenshot)
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
                #fit = fitnessTracker.getFitness() * 2
                #fit = max((fit - fitnessPenaltySub) * fitnessPenaltyMult, 0)
                fit = max(round(newFitness / 3) - fitnessPenaltySub, 0)
                brains.assignFitness(fit)
                print('Fitness: ' + str(fit) + ' (game over)')
                restartRun()

            # program completes the level
            if (imageCheck.checkLevelComplete(grayimg)):
                endRun()
                #fit = ((constants.TOTAL_TIMEOUT * 2) - fitnessTracker.getFitness()) * 2
                #fit = max((fit - fitnessPenaltySub) * fitnessPenaltyMult, 0)
                fit = max(round(newFitness / 3) - fitnessPenaltySub, 0)
                brains.assignFitness(fit)
                print('Fitness: ' + str(fit) + ' (level complete)')
                restartRun()

            # program stops making progress
            if (checkProgress and imageCheck.checkNoProgress(grayimg)):
                endRun()
                #fit = (fitnessTracker.getFitness() - (constants.PROGRESS_CHECK_TIMEOUT * 1.5)) * 2
                #fit = max((fit - fitnessPenaltySub) * fitnessPenaltyMult, 0)
                fit = max(round(newFitness / 3) - fitnessPenaltySub, 0)
                if (imageCheck.checkEarlyOut(grayimg)):
                    fit = 0
                brains.assignFitness(fit)
                print('Fitness: ' + str(fit) + ' (no progress)')
                restartRun()

            # program stops controlling character
            if (controlTimer.timeUp() and imageCheck.checkNoControl(grayimg)):
                endRun()
                #fit = (fitnessTracker.getFitness() - constants.CONTROL_TIMEOUT) * 2
                #fit = max((fit - fitnessPenaltySub) * fitnessPenaltyMult, 0)
                fit = max(round(newFitness / 3) - fitnessPenaltySub, 0)
                if (imageCheck.checkEarlyOut(grayimg)):
                    fit = 0
                brains.assignFitness(fit)
                print('Fitness: ' + str(fit) + ' (no control)')
                restartRun()

            # program times out
            if (globalTimer.timeUp()):
                endRun()
                #fit = 0
                fit = max(round(newFitness / 3) - fitnessPenaltySub, 0)
                brains.assignFitness(fit)
                print('Fitness: ' + str(fit) + ' (time out)')
                restartRun()

        #print('screen translated by ' + str(imageCheck.checkScreenTranslation(screenshot)))
        v = imageCheck.checkScreenTranslation(screenshot)
        #print(v)
        newFitness -= v#imageCheck.checkScreenTranslation(screenshot)

        nextTick = nextTick + timedelta(microseconds=100000)


############################ safe shut down #############################
finally:
    controller.cutoffInputs()
    keyListener.stop()
    globalTimer.cancelTimer()
    progressCheckTimer.cancelTimer()
    controlTimer.cancelTimer()
    controlImageTimer.cancelTimer()

    '''
    timeAve = 0
    for t in range(len(timeList) - 1):
        diff = abs(timeList[t] - timeList[t + 1])
        timeAve = timeAve + diff
    print('ave time diff: ' + str(timeAve/(len(timeList) - 1)))
    '''


if saveProgress:
    with open(constants.SAVE_FILE_NAME, 'wb') as output:
        pickle.dump(brains, output, pickle.HIGHEST_PROTOCOL)
        c = [brain.nodeCount, brain.connectionCount, ga.speciesCounter]
        pickle.dump(c,output,pickle.HIGHEST_PROTOCOL)
        print('Population saved')
