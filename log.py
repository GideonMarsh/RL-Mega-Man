# Gideon Marsh
# github.com/GideonMarsh

import ga
import constants

def writeToLog(brains):

    meanFitness = 0
    fitnesses = list()
    for p in range(len(brains.population)):
        individual = brains.population[p]
        fitnesses.append(individual.fitness / len(brains.species[individual.species]))
        meanFitness = meanFitness + fitnesses[p]
    meanFitness = meanFitness / len(brains.population)

    newSizes = {}
    totalPopulation = 0
    for key in brains.species.keys():
        sumFitness = 0
        for p in range(len(brains.population)):
            if (brains.population[p].species == key):
                sumFitness = sumFitness + fitnesses[p]
        newSizes[key] = round(sumFitness / meanFitness)
        totalPopulation = totalPopulation + round(sumFitness / meanFitness)

    excessPopulation = totalPopulation - 100

    while (excessPopulation > 0):
        ns = list(newSizes.keys())
        ns.sort(reverse = True)
        for k in ns:
            if (newSizes[k] > 0):
                newSizes[k] = newSizes[k] - 1
                excessPopulation = excessPopulation - 1
                if (excessPopulation <= 0):
                    break

    while (excessPopulation < 0):
        ns = list(newSizes.keys())
        ns.sort()
        for k in ns:
            if (newSizes[k] > 0):
                newSizes[k] = newSizes[k] + 1
                excessPopulation = excessPopulation + 1
                if excessPopulation >= 0:
                    break

    l = ['Generation ' + str(brains.generation),'','Number of species: ' + str(len(brains.species.keys()))]

    for k in brains.species.keys():
        l.append('')
        aveFitness = 0
        for i in brains.species[k]:
            sumFitness = sumFitness + i.fitness
        aveFitness = aveFitness / len(brains.species[k])
        l.append('Species ' + str(k) + '    Species size: ' + str(len(brains.species[k])) + '    Average fitness: ' + str(aveFitness))
        newLine = 0
        for i in range(len(brains.population)):
            if brains.population[i].species == k:
                if newLine == 0:
                    l.append(str(i) + ' ' + str(brains.population[i].fitness))
                else:
                    l[-1] = l[-1] + '     ' + str(i) + ' ' + str(brains.population[i].fitness)
                newLine = (newLine + 1) % 5
        l.append('Number of new children: ' + str(newSizes[k]))

    l.append('')
    l.append('')

    file = open(constants.LOG_FILE_NAME, 'a')
    for s in l:
        file.write(s + '\n')
    file.close()
