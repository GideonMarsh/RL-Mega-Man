# Gideon Marsh
# github.com/GideonMarsh

from PIL import Image

class GeneticAlgorithmController:
    def __init__(self, popSize, mutationChance, maxGenerations):
        self.population = list()
        self.mutationChance = mutationChance
        self.maxGenerations = maxGenerations


    def passInputs(self, image):
