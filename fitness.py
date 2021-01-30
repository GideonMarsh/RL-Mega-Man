# Gideon Marsh
# github.com/GideonMarsh

from time import time
from threading import Timer

class FitnessTimer:
    startTime = 0
    endTime = 0

    def setStartTime():
        startTime = time.time()
        endTime = startTime

    def setEndTime():
        endTime = time.time()

    def getTimeElapsed():
        return endTime - startTime


class RunTimer:
    def __init__(self,minutes):
        self.t = Timer(minutes * 60, self.timeUp)
        self.ended = False

    def startTimer(self):
        self.t.start()

    def timeUp(self):
        self.ended = True

    def cancelTimer(self):
        self.t.cancel()

    def isTimeUp(self):
        return self.ended
