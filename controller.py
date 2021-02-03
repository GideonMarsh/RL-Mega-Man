# Gideon Marsh
# github.com/GideonMarsh

from pynput.keyboard import Key, Controller
from time import sleep

keyboard = Controller()

def loadSave():
    sleep(0.06)
    keyboard.press('`')
    sleep(0.03)
    keyboard.release('`')
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

def closeMenu():
    keyboard.press(Key.esc)
    sleep(0.03)
    keyboard.release(Key.esc)

# game controls are received in a list in the following order:
# up, right, down, left, jump, shoot
# if input is greater than 0, button is pressed
def changeInputs(inputs):
    if (inputs[0] > 0):
        keyboard.press(Key.up)
    else:
        keyboard.release(Key.up)
    if (inputs[1] > 0):
        keyboard.press(Key.right)
    else:
        keyboard.release(Key.right)
    if (inputs[2] > 0):
        keyboard.press(Key.down)
    else:
        keyboard.release(Key.down)
    if (inputs[3] > 0):
        keyboard.press(Key.left)
    else:
        keyboard.release(Key.left)
    if (inputs[4] > 0):
        keyboard.press('x')
    else:
        keyboard.release('x')
    if (inputs[5] > 0):
        keyboard.press('z')
    else:
        keyboard.release('z')

def cutoffInputs():
    keyboard.release(Key.up)
    keyboard.release(Key.right)
    keyboard.release(Key.down)
    keyboard.release(Key.left)
    keyboard.release('x')
    keyboard.release('z')
