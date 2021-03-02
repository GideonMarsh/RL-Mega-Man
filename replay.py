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

stage = 'air_man'
onlyBests = True
generation = 0

############################# initial setup #############################
'''
Manual steps to take before running program:
1. Make sure all checkpoint images are saved and ready for comparison
2. Save the game at the start of the level that is being played immediately after Mega Man becomes controllable
3. Navigate to a menu without a black background (stage select works)
4. Open options menu (cursor should be on 'SAVE GAME')
5. Start program

Press 'w' or 't' to end program
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
fitnessPenalty = 0

imageCheck = imagechecker.ImageChecker()
imageCheck.imageSetup()

continueGame = True

globalTimer = fitness.RunTimer(constants.TOTAL_TIMEOUT)
progressCheckTimer = fitness.RunTimer(constants.PROGRESS_CHECK_EARLY_TIMEOUT)
controlTimer = fitness.RunTimer(constants.CONTROL_TIMEOUT)
controlImageTimer = fitness.RunTimer(2)
checkProgress = False

grayimg = None

firstImageTaken = False
controlImageTaken = False

firstRunDone = False

if onlyBests:
    generation = 0
saveName = 'saves/' + stage + '/Generation_' + str(generation) + '.pkl'

# check if saved population exists and load it
# if none exists, create new population from the beginning
brains = None
if path.exists(saveName):
    with open(saveName, 'rb') as input:
        brains = pickle.load(input)
        brains.currentBrain = 0
        c = pickle.load(input)
        brain.nodeCount = c[0]
        brain.connectionCount = c[1]
        ga.speciesCounter = c[2]
        print('Population loaded')
else:
    print('No saved population found')

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
    except AttributeError:
        pass

# call this function before the start of every run
def restartRun():
    global globalTimer, currentlyPlaying, progressCheckTimer, checkProgress, firstImageTaken, controlTimer, controlImageTimer, controlImageTaken, fitnessPenalty, brains, generation, firstRunDone, nextTick
    globalTimer.cancelTimer()
    progressCheckTimer.cancelTimer()
    controlTimer.cancelTimer()
    controlImageTimer.cancelTimer()
    globalTimer = fitness.RunTimer(constants.TOTAL_TIMEOUT)
    progressCheckTimer = fitness.RunTimer(constants.PROGRESS_CHECK_EARLY_TIMEOUT)
    controlTimer = fitness.RunTimer(constants.CONTROL_TIMEOUT)
    controlImageTimer = fitness.RunTimer(2)
    fitnessPenalty = 0

    if firstRunDone:
        if onlyBests:
            generation = generation + 1
            saveName = 'saves/' + stage + '/Generation_' + str(generation) + '.pkl'
            if path.exists(saveName):
                with open(saveName, 'rb') as input:
                    brains = pickle.load(input)
                    brains.currentBrain = 0
                    c = pickle.load(input)
                    brain.nodeCount = c[0]
                    brain.connectionCount = c[1]
                    ga.speciesCounter = c[2]
                    print('Population loaded')
            else:
                continueGame = False
                print('All Populations Played')
        else:
            brains.currentBrain = brains.currentBrain + 1
            if brains.currentBrain >= constants.POPULATION_SIZE:
                continueGame = False
    else:
        firstRunDone = True

    if onlyBests:
        print('Generation ' + str(brains.getIndividualInfo()[0]) + ' Best Performer; Species ' + str(brains.bestBrain.species))
    else:
        print('Generation ' + str(brains.getIndividualInfo()[0]) + '; Species ' + str(brains.getIndividualInfo()[1]) + '; Player ' + str(brains.getIndividualInfo()[2]))
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
    nextTick = datetime.now() + timedelta(microseconds=100000)

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
try:
    restartRun()
    while (continueGame and not screenshotter.isProgramOver(constants.WINDOWNAME)):
        # wait for the next tick
        while (datetime.now() < nextTick):
            pass
        screenshot = screenshotter.takescreenshot(constants.WINDOWNAME, region)

        '''
        now = datetime.now().microsecond
        print(str(now) + ' ' + str(nextTick))
        '''

        if (screenshot):
            grayimg = screenshot.convert('L')

            if onlyBests:
                outputChange = controller.changeInputs(brains.passInputs(grayimg, brains.bestBrain))
            else:
                outputChange = controller.changeInputs(brains.passInputs(grayimg))

            if outputChange:
                fitnessPenalty = fitnessPenalty + constants.CONTROL_FITNESS_PENALTY
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
                fit = max(fit - fitnessPenalty, 0) * 2
                print('Fitness: ' + str(fit) + ' (game over)')
                if onlyBests:
                    if (fit < brains.bestBrain.fitness):
                        print('Major Fitness mismatch! Original: ' + str(brains.bestBrain.fitness) + ' New: ' + str(fit))
                    if (fit > brains.bestBrain.fitness):
                        print('Minor mismatch (Original: ' + str(brains.bestBrain.fitness) + ' New: ' + str(fit) + ')')
                else:
                    if (fit < brains.population[brains.currentBrain].fitness):
                        print('Major Fitness mismatch! Original: ' + brains.population[brains.currentBrain].fitness + ' New: ' + str(fit))
                    if (fit > brains.population[brains.currentBrain].fitness):
                        print('Minor mismatch (Original: ' + brains.population[brains.currentBrain].fitness + ' New: ' + str(fit) + ')')
                restartRun()

            # program completes the level
            if (imageCheck.checkLevelComplete(grayimg)):
                endRun()
                fit = (constants.TOTAL_TIMEOUT * 2) - fitnessTracker.getFitness()
                fit = max(fit - fitnessPenalty, 0) * 2
                print('Fitness: ' + str(fit) + ' (level complete)')
                if onlyBests:
                    if (fit < brains.bestBrain.fitness):
                        print('Major Fitness mismatch! Original: ' + str(brains.bestBrain.fitness) + ' New: ' + str(fit))
                    if (fit > brains.bestBrain.fitness):
                        print('Minor mismatch (Original: ' + str(brains.bestBrain.fitness) + ' New: ' + str(fit) + ')')
                else:
                    if (fit < brains.population[brains.currentBrain].fitness):
                        print('Major Fitness mismatch! Original: ' + brains.population[brains.currentBrain].fitness + ' New: ' + str(fit))
                    if (fit > brains.population[brains.currentBrain].fitness):
                        print('Minor mismatch (Original: ' + brains.population[brains.currentBrain].fitness + ' New: ' + str(fit) + ')')
                restartRun()

            # program stops making progress
            if (checkProgress and imageCheck.checkNoProgress(grayimg)):
                endRun()
                fit = fitnessTracker.getFitness() - (constants.PROGRESS_CHECK_TIMEOUT * 1.5)
                fit = max(fit - fitnessPenalty, 0) * 2
                if (imageCheck.checkEarlyOut(grayimg)):
                    fit = 0
                print('Fitness: ' + str(fit) + ' (no progress)')
                if onlyBests:
                    if (fit < brains.bestBrain.fitness):
                        print('Major Fitness mismatch! Original: ' + str(brains.bestBrain.fitness) + ' New: ' + str(fit))
                    if (fit > brains.bestBrain.fitness):
                        print('Minor mismatch (Original: ' + str(brains.bestBrain.fitness) + ' New: ' + str(fit) + ')')
                else:
                    if (fit < brains.population[brains.currentBrain].fitness):
                        print('Major Fitness mismatch! Original: ' + brains.population[brains.currentBrain].fitness + ' New: ' + str(fit))
                    if (fit > brains.population[brains.currentBrain].fitness):
                        print('Minor mismatch (Original: ' + brains.population[brains.currentBrain].fitness + ' New: ' + str(fit) + ')')
                restartRun()

            # program stops controlling character
            if (controlTimer.timeUp() and imageCheck.checkNoControl(grayimg)):
                endRun()
                fit = fitnessTracker.getFitness() - constants.CONTROL_TIMEOUT
                fit = max(fit - fitnessPenalty, 0) * 2
                if (imageCheck.checkEarlyOut(grayimg)):
                    fit = 0
                print('Fitness: ' + str(fit) + ' (no control)')
                if onlyBests:
                    if (fit < brains.bestBrain.fitness):
                        print('Major Fitness mismatch! Original: ' + str(brains.bestBrain.fitness) + ' New: ' + str(fit))
                    if (fit > brains.bestBrain.fitness):
                        print('Minor mismatch (Original: ' + str(brains.bestBrain.fitness) + ' New: ' + str(fit) + ')')
                else:
                    if (fit < brains.population[brains.currentBrain].fitness):
                        print('Major Fitness mismatch! Original: ' + brains.population[brains.currentBrain].fitness + ' New: ' + str(fit))
                    if (fit > brains.population[brains.currentBrain].fitness):
                        print('Minor mismatch (Original: ' + brains.population[brains.currentBrain].fitness + ' New: ' + str(fit) + ')')
                restartRun()

            # program times out
            if (globalTimer.timeUp()):
                endRun()
                fit = 0
                print('Fitness: ' + str(fit) + ' (time out)')
                if onlyBests:
                    if (fit < brains.bestBrain.fitness):
                        print('Major Fitness mismatch! Original: ' + str(brains.bestBrain.fitness) + ' New: ' + str(fit))
                    if (fit > brains.bestBrain.fitness):
                        print('Minor mismatch (Original: ' + str(brains.bestBrain.fitness) + ' New: ' + str(fit) + ')')
                else:
                    if (fit < brains.population[brains.currentBrain].fitness):
                        print('Major Fitness mismatch! Original: ' + brains.population[brains.currentBrain].fitness + ' New: ' + str(fit))
                    if (fit > brains.population[brains.currentBrain].fitness):
                        print('Minor mismatch (Original: ' + brains.population[brains.currentBrain].fitness + ' New: ' + str(fit) + ')')
                restartRun()

        nextTick = nextTick + timedelta(microseconds=100000)


############################ safe shut down #############################
finally:
    controller.cutoffInputs()
    keyListener.stop()
    globalTimer.cancelTimer()
    progressCheckTimer.cancelTimer()
    controlTimer.cancelTimer()
    controlImageTimer.cancelTimer()
