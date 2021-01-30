# Gideon Marsh
# github.com/GideonMarsh

import pyautogui
import win32gui
import time
import math

def takescreenshot(windowName=None, r=None):
    if r:
        hwnd = win32gui.FindWindow(None, windowName)
        if hwnd:
            x, y, x1, y1 = win32gui.GetClientRect(hwnd)
            x, y = win32gui.ClientToScreen(hwnd, (x, y))
            im = pyautogui.screenshot(region=(r[0] + x,r[1] + y,r[2],r[3]))
            return im
        else:
            print('Window not found!')
    else:
        im = pyautogui.screenshot()
        return im

def findBounds(windowName=None):
    if windowName:
        hwnd = win32gui.FindWindow(None, windowName)
        if hwnd:
            win32gui.SetForegroundWindow(hwnd)
            x, y, x1, y1 = win32gui.GetClientRect(hwnd)
            x, y = win32gui.ClientToScreen(hwnd, (x, y))
            x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
            im = pyautogui.screenshot(region=(x, y, x1, y1))

            pix = im.load()
            bx = by = bw = bh = 0
            previous = (0,0,0)
            for i in range(x1):
                if (previous != pix[i,math.floor(y1 / 2)]):
                    bx = i
                    break
            previous = (0,0,0)
            for i in range(y1):
                if (previous != pix[math.floor(x1 / 2),i]):
                    by = i
                    break
            previous = (0,0,0)
            for i in range(x1):
                if (previous != pix[x1 - i - 1,math.floor(y1 / 2)]):
                    bw = (x1 - i) - bx
                    break
            previous = (0,0,0)
            for i in range(y1):
                if (previous != pix[math.floor(x1 / 2),y1 - i - 1]):
                    bh = (y1 - i) - by
                    break

            return (bx, by, bw, bh)
        else:
            print("Window not found!")
    else:
        print("Window needs a name!")

def setWindowSize(windowName=None,width=1920, height=1080):
    if windowName:
        hwnd = win32gui.FindWindow(None, windowName)
        if hwnd:
            win32gui.SetForegroundWindow(hwnd)
            win32gui.MoveWindow(hwnd, 0, 0, width, height, True)
        else:
            print("Window not found!")
    else:
        print("Window needs a name!")

def isProgramOver(windowName=None):
    if windowName:
        hwnd = win32gui.FindWindow(None, windowName)
        hwndCheck = win32gui.GetForegroundWindow()
        if (hwnd == hwndCheck):
            return False
        return True
    else:
        return True
