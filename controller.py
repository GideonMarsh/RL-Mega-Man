# Gideon Marsh
# github.com/GideonMarsh

from pynput.keyboard import Key, Controller
from time import sleep

keyboard = Controller()

keysPressed = [0,0,0,0,0,0]

def loadSave():
    sleep(0.06)
    keyboard.press(Key.down)
    sleep(0.03)
    keyboard.release(Key.down)
    sleep(0.06)
    keyboard.press(Key.enter)
    sleep(0.03)
    keyboard.release(Key.enter)
    sleep(0.06)
    keyboard.press(Key.right)
    sleep(0.03)
    keyboard.release(Key.right)
    sleep(0.06)
    keyboard.press(Key.enter)
    sleep(0.03)
    keyboard.release(Key.enter)
    sleep(0.06)
    keyboard.press(Key.enter)
    sleep(0.03)
    keyboard.release(Key.enter)
    sleep(0.06)
    keyboard.press(Key.esc)
    sleep(0.03)
    keyboard.release(Key.esc)
    sleep(0.06)

def openMenu():
    sleep(0.01)
    keyboard.press('`')
    sleep(0.03)
    keyboard.release('`')
    sleep(0.01)

def closeMenu():
    sleep(0.01)
    keyboard.press(Key.esc)
    sleep(0.03)
    keyboard.release(Key.esc)
    sleep(0.01)

# game controls are received in a list in the following order:
# up, right, down, left, jump, shoot
# if input is greater than 0, button is pressed
# returns true if an input changed, false otherwise
def changeInputs(inputs):
    global keysPressed
    k = [0,0,0,0,0,0]
    if (inputs[0] > 0):
        keyboard.press(Key.up)
        k[0] = 1
    else:
        keyboard.release(Key.up)
    if (inputs[1] > 0):
        keyboard.press(Key.right)
        k[1] = 1
    else:
        keyboard.release(Key.right)
    if (inputs[2] > 0):
        keyboard.press(Key.down)
        k[2] = 1
    else:
        keyboard.release(Key.down)
    if (inputs[3] > 0):
        keyboard.press(Key.left)
        k[3] = 1
    else:
        keyboard.release(Key.left)
    if (inputs[4] > 0):
        keyboard.press('x')
        k[4] = 1
    else:
        keyboard.release('x')
    if (inputs[5] > 0):
        keyboard.press('z')
        k[5] = 1
    else:
        keyboard.release('z')
    if not k == keysPressed:
        keysPressed = k
        return True
    return False

def cutoffInputs():
    keyboard.release(Key.up)
    keyboard.release(Key.right)
    keyboard.release(Key.down)
    keyboard.release(Key.left)
    keyboard.release('x')
    keyboard.release('z')
    keysPressed = (0,0,0,0,0,0)
