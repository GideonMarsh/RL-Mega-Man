# Gideon Marsh
# github.com/GideonMarsh

import brain
import constants
from PIL import Image
from math import floor
from random import random

class GeneticAlgorithmController:
    def __init__(self, popSize, idealSpecies, mutationChance):
        # The whole population in an unordered list
        self.population = list()
        # A 2d list of the population, where the first index is species
        self.species = list()
        self.mutationChance = mutationChance
        self.generation = 0
        self.currentBrain = 0
        self.delta = constants.STARTING_DELTA
        self.idealSpecies = idealSpecies

        for i in range(popSize):
            newBrain = brain.Brain()
            newBrain.initNewBrain()

            newBrain.prepareNodeTopology()
            self.population.append(newBrain)

        self.separateIntoSpecies()

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
        randomly mutate every individual with a certain probability

        4. separate the new population into species
        (create new species when necessary)
        '''

        # step 1
        meanFitness = 0
        for s in self.species:
            for i in s:
                i.fitness = i.fitness / len(s)
                meanFitness = meanFitness + i.fitness
        meanFitness = meanFitness / len(self.population)

        # step 2
        newSizes = {}
        for s in range(len(self.species)):
            sumFitness = 0
            for i in self.species[s]:
                sumFitness = sumFitness + i.fitness
            newSizes[s] = round(sumFitness / meanFitness)

        # step 3
        def fitnessSort(i):
            return i.fitness

        newPopulation = list()

        for s in range(len(self.species)):
            if (newSizes[s] > 0):
                self.species[s].sort(key=fitnessSort, reverse=True)
                eligibleParents = list()
                for i in range(max(1, round(len(self.species[s]) * constants.ACCEPTABLE_PARENTS_PERCENTAGE))):
                    eligibleParents.append(self.species[s][i])
                for i in range(newSizes[s]):
                    # just choose two from the eligible parents with replacement
                    parent1 = eligibleParents[floor(random() * len(eligibleParents))]
                    parent2 = eligibleParents[floor(random() * len(eligibleParents))]
                    newBrain = brain.Brain()
                    newBrain.crossover(parent1, parent2)
                    newPopulation.append(newBrain)

        for p in newPopulation:
            if (random() < self.mutationChance):
                p.mutateStructure()
            if (random() < self.mutationChance):
                p.mutateWeights()
            p.prepareNodeTopology()

        self.population = newPopulation

        # step 4
        self.separateIntoSpecies()

        self.currentBrain = 0
        self.generation = self.generation + 1

    def getIndividualInfo(self):
        return (self.generation, self.currentBrain)

    # separates population into species
    def separateIntoSpecies(self):
        self.species = list()
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
        difference = len(self.species) - self.idealSpecies  # keep the sign of this value for addition to delta
        deltaChange = difference * abs(difference) * 0.01
        self.delta = max(round(self.delta + deltaChange, 0.01)

brains = GeneticAlgorithmController(100, 6, constants.MUTATION_CHANCE)

print(len(brains.population))
print(len(brains.species))
print(brains.delta)

for i in range(20):
    while not brains.doneWithGeneration():
        brains.assignFitness(round(random() * 100, 2))

    brains.makeNextGeneration()
    print(len(brains.population))
    print(len(brains.species))
    print(brains.delta)
