# Gideon Marsh
# github.com/GideonMarsh

from PIL import Image
from math import floor

def checkGameOver(image=None, xp=266, yp=200):
    gameOver = Image.open('game_over_screen.png')
    pix = image.load()
    gopix = gameOver.load()

    xOffset = floor(image.width / xp)
    yOffset = floor(image.height / yp)
    xShift = floor((image.width % xp) / 2)
    yShift = floor((image.height % yp) / 2)

    for i in range(xp):
        for j in range(yp):
            if (pix[(i * xOffset) + xShift, (j * yOffset) + yShift] != gopix[(i * xOffset) + xShift, (j * yOffset) + yShift]):
                return False

    return True
