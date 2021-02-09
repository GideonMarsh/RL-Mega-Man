# Gideon Marsh
# github.com/GideonMarsh

import brain
import constants
from PIL import Image
from math import floor
from random import random
from time import time

speciesCounter = 0

class GeneticAlgorithmController:
    def __init__(self, popSize, idealSpecies, mutationChance):
        # The whole population in an unordered list
        self.population = list()
        # A 2d list of the population, where the first index is species
        self.species = {}
        self.mutationChance = mutationChance
        self.generation = 0
        self.currentBrain = 0
        self.idealSpecies = idealSpecies
        self.delta = constants.STARTING_DELTA
        self.bestBrain = None

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
                inputs.append(pix[(i * xOffset) + xShift, (j * yOffset) + yShift] - 128)

        return self.population[self.currentBrain].think(inputs)

    # assign fitness and set current brain to next brain
    # treat all negative fitness values as 0
    def assignFitness(self, fitness):
        if (fitness < 0):
            self.population[self.currentBrain].fitness = 0
        else:
            self.population[self.currentBrain].fitness = fitness
        if (not self.bestBrain or self.bestBrain.fitness < fitness):
            self.bestBrain = self.population[self.currentBrain]
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
        limit the amount of new organisms to the max population size by randomly but evenly lowering each species size

        3. create new generation
        for each species, select the highest r% of the species to breed
        randomly breed a number of offspring equal to the newSpeciesSize
        randomly mutate every individual with a certain probability

        4. separate the new population into species
        (create new species when necessary)


        NOTE: generations will have far too many individuals if any individuals from the previous generation had negative fitness
        This is not designed to work with negative fitness values
        '''

        # step 1
        meanFitness = 0
        for specie in self.species.values():
            for individual in specie:
                individual.fitness = individual.fitness / len(specie)
                meanFitness = meanFitness + individual.fitness
        meanFitness = meanFitness / len(self.population)

        # step 2
        newSizes = {}
        totalPopulation = 0
        for key in self.species.keys():
            sumFitness = 0
            for individual in self.species[key]:
                sumFitness = sumFitness + individual.fitness
            newSizes[key] = round(sumFitness / meanFitness)
            totalPopulation = totalPopulation + round(sumFitness / meanFitness)

        # add or remove to the species' sizes to make the population exactly 100
        excessPopulation = totalPopulation - 100

        while (excessPopulation > 0):
            # remove one individual from each species, starting with the most populous ones
            ns = list(newSizes.keys())
            ns.sort(reverse = True)
            for k in ns:
                if (newSizes[k] > 0):
                    newSizes[k] = newSizes[k] - 1
                    excessPopulation = excessPopulation - 1
                    if (excessPopulation <= 0):
                        break

        while (excessPopulation < 0):
            # add one individual to each species, starting with the smallest ones
            ns = list(newSizes.keys())
            ns.sort()
            for k in ns:
                if (newSizes[k] > 0):
                    newSizes[k] = newSizes[k] + 1
                    excessPopulation = excessPopulation + 1
                    if excessPopulation >= 0:
                        break

        # remove 1 from the species containing the best brain, to make room for the best brain to carry over
        newSizes[self.bestBrain.species] = newSizes[self.bestBrain.species] - 1

        # step 3
        def fitnessSort(i):
            return i.fitness

        newPopulation = list()

        for key in self.species.keys():
            if (newSizes[key] > 0):
                self.species[key].sort(key=fitnessSort, reverse=True)
                eligibleParents = list()
                for i in range(max(1, round(len(self.species[key]) * constants.ACCEPTABLE_PARENTS_PERCENTAGE))):
                    eligibleParents.append(self.species[key][i])

                for i in range(newSizes[key]):
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
        brain = self.population[self.currentBrain]
        return (self.generation, brain.species, self.currentBrain)


    def getBestInfo(self):
        return (self.bestBrain.species, self.bestBrain.fitness)

    # separates population into species
    def initialSeparateIntoSpecies(self):
        for g in self.population:
            speciesFound = False
            # check if g should be part of this species
            for specie in self.species.keys():
                i = floor(len(self.species[specie]) * random())
                d = g.compare(self.species[specie][i])
                if (d <= self.delta):
                    self.species[specie].append(g)
                    g.species = specie
                    speciesFound = True
                    break
            # no existing species has accepted g, so add as a new species
            if not speciesFound:
                global speciesCounter
                self.species[speciesCounter] = list()
                self.species[speciesCounter].append(g)
                g.species = speciesCounter
                speciesCounter = speciesCounter + 1
        '''
        # modify self.delta based on the difference between number of species and desired number of species
        difference = len(self.species.values()) - self.idealSpecies  # keep the sign of this value for addition to delta
        self.delta = self.delta + (difference * 0.001)
        '''

    def separateIntoSpecies(self):
        oldSpecies = self.species.copy()

        for s in oldSpecies.keys():
            oldSpecies[s] = oldSpecies[s].copy()
        for g in self.population:
            speciesFound = False
            # check if g should be part of this species
            for specie in self.species.keys():
                i = floor(len(self.species[specie]) * random())
                d = g.compare(self.species[specie][i])
                if (d <= self.delta):
                    self.species[specie].append(g)
                    g.species = specie
                    speciesFound = True
                    break
            # no existing species has accepted g, so add as a new species
            if not speciesFound:
                global speciesCounter
                self.species[speciesCounter] = list()
                self.species[speciesCounter].append(g)
                g.species = speciesCounter
                speciesCounter = speciesCounter + 1

        # remove the old population from the species list except for the best brain
        for oldSpecie in oldSpecies.values():
            for brain in oldSpecie:
                if (not brain == self.bestBrain):
                    for specie in self.species.values():
                        if brain in specie:
                            specie.remove(brain)
                            break

        self.population.append(self.bestBrain)

        speciesToRemove = list()
        for specie in self.species.keys():
            if (len(self.species[specie]) == 0):
                speciesToRemove.append(specie)


        for i in speciesToRemove:
            self.species.pop(i)

        # modify self.delta based on the difference between number of species and desired number of species
        difference = len(self.species.values()) - self.idealSpecies  # keep the sign of this value for addition to delta
        difference = difference * abs(difference)
        if difference < 0:
            difference = difference * 2
        self.delta = self.delta + (difference * 0.0001)

'''
brains = GeneticAlgorithmController(100, 25, constants.MUTATION_CHANCE)

print(brains.generation)
print(len(brains.population))
print(len(brains.species))
print(brains.delta)

for i in range(100):
    while not brains.doneWithGeneration():
        image = Image.open('images/respawn_air_man_1.png')
        outputs = brains.passInputs(image)
        fit = 0
        for o in outputs:
            fit = fit + o
        if fit < 0:
            fit = 0
        brains.assignFitness(fit)

    print('best: ' + str(brains.getBestInfo()[0]) + ' ' + str(brains.getBestInfo()[1]))
    for s in brains.species.keys():
        print(str(s) + ' ' + str(len(brains.species[s])),end='; ')
    print(' ')
    print(' ')

    brains.makeNextGeneration()
    print(brains.generation)
    print(len(brains.population))
    print(len(brains.species))
    print(brains.delta)

while not brains.doneWithGeneration():
    image = Image.open('images/respawn_air_man_1.png')
    outputs = brains.passInputs(image)
    fit = 0
    for o in outputs:
        fit = fit + o
    brains.assignFitness(fit)

print('best: ' + str(brains.getBestInfo()[0]) + ' ' + str(brains.getBestInfo()[1]))
for s in brains.species.keys():
    print(str(s) + ' ' + str(len(brains.species[s])),end='; ')
print(' ')
'''
