# Gideon Marsh
# github.com/GideonMarsh

import brain
import constants
from PIL import Image
from math import floor

class GeneticAlgorithmController:
    def __init__(self, popSize, mutationChance, maxGenerations):
        self.basePopulation = list()
        self.mutationChance = mutationChance
        self.maxGenerations = maxGenerations
        self.currentBrain = 0

        for i in range(popSize):
            newBrain = brain.Brain()
            newBrain.initNewBrain()

            newBrain.prepareNodeTopology()
            self.basePopulation.append(newBrain)


    def passInputs(self, image):
        pix = image.load()

        xOffset = floor(image.width / constants.XPIXELS)
        yOffset = floor(image.height / constants.YPIXELS)
        xShift = floor((image.width % constants.XPIXELS) / 2)
        yShift = floor((image.height % constants.YPIXELS) / 2)

        inputs = list()
        for i in range(constants.XPIXELS):
            for j in range(constants.YPIXELS):
                inputs.append(pix[(i * xOffset) + xShift, (j * yOffset) + yShift])

        return self.basePopulation[self.currentBrain].think(inputs)

    # assign fitness and set current brain to next brain
    def assignFitness(self, fitness):
        self.basePopulation[self.currentBrain].fitness = fitness
        self.currentBrain = self.currentBrain + 1

    def doneWithGeneration(self):
        return self.currentBrain >= len(self.basePopulation)

    def makeNextGeneration(self):
        self.currentBrain = 0

    def getIndividualInfo(self):
        return self.currentBrain
