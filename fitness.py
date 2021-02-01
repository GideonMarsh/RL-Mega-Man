# Gideon Marsh
# github.com/GideonMarsh

from time import time
from threading import Timer

class FitnessTimer:
    def __init__(self):
        self.startTime = 0
        self.endTime = 0
        self.running = False

    def setStartTime(self):
        self.startTime = time()
        self.endTime = self.startTime
        self.running = True

    def setEndTime(self):
        self.endTime = time()
        self.running = False

    def getFitness(self):
        if (self.running):
            return round(time() - self.startTime, 1)
        else:
            return round(self.endTime - self.startTime, 1)

    def isRunning(self):
        return self.running


def timeOver(e):
    e.ended = True

class RunTimer:
    def __init__(self,seconds):
        self.ended = False
        self.t = Timer(seconds, timeOver, [self])

    def startTimer(self):
        self.t.start()

    def cancelTimer(self):
        self.t.cancel()

    def timeUp(self):
        return self.ended
