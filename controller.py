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
