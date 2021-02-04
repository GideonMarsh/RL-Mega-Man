# Gideon Marsh
# github.com/GideonMarsh

import brain
import constants
from PIL import Image
from math import floor
from random import random

class GeneticAlgorithmController:
    def __init__(self, popSize, idealSpecies, mutationChance, maxGenerations):
        # The whole population in an unordered list
        self.population = list()
        # A 2d list of the population, where the first index is species
        self.species = list()
        self.mutationChance = mutationChance
        self.maxGenerations = maxGenerations
        self.currentBrain = 0
        self.delta = constants.STARTING_DELTA
        self.idealSpecies = idealSpecies

        for i in range(popSize):
            newBrain = brain.Brain()
            newBrain.initNewBrain()

            newBrain.prepareNodeTopology()
            self.population.append(newBrain)

        self.initialSeparateIntoSpecies()

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

        return self.population[self.currentBrain].think(inputs)

    # assign fitness and set current brain to next brain
    def assignFitness(self, fitness):
        self.population[self.currentBrain].fitness = fitness
        self.currentBrain = self.currentBrain + 1

    def doneWithGeneration(self):
        return self.currentBrain >= len(self.population)

    def makeNextGeneration(self):
        '''
        steps:

        1. adjust fitness by species size
        adjustedFitness = fitness / speciesSize

        2. apportion new species sizes of next generation
        newSpeciesSize = (sum of all adjusted fitnesses) / (mean adjusted fitness of entire population)

        3. create new generation
        for each species, select the highest r% of the species to breed
        randomly breed a number of offspring equal to the newSpeciesSize

        4. separate the new population into species based on the old population's species
        (create new species when necessary)
        '''
        self.currentBrain = 0

    def getIndividualInfo(self):
        return self.currentBrain

    # separates initial population into species
    # should only be called in constructor
    def initialSeparateIntoSpecies(self):
        for g in self.population:
            speciesFound = False
            specie = 0
            while (not speciesFound):
                if (len(self.species) <= specie):
                    # no existing species has accepted g, so add as a new species
                    self.species.append(list())
                    self.species[specie].append(g)
                    speciesFound = True
                else:
                    # check if g should be part of this species
                    i = floor(len(self.species[specie]) * random())
                    d = g.compare(self.species[specie][i])
                    if (d <= self.delta):
                        self.species[specie].append(g)
                        speciesFound = True
                    specie = specie + 1

        # modify self.delta based on the difference between number of species and desired number of species
        self.delta = max(self.delta + ((self.idealSpecies - len(self.species)) * 0.01), 0.01)

    # separates the current population into species based on the previous population
    def separateIntoSpecies(self):
        pass


#brains = GeneticAlgorithmController(100, 6, constants.MUTATION_CHANCE, 100)
