# Gideon Marsh
# github.com/GideonMarsh


from screenshotter import takescreenshot
from screenshotter import findBounds
import math
import time
#screenshot = takescreenshot('Mega Man Legacy Collection')

#hwnd = win32gui.FindWindow(None, 'Mega Man Legacy Collection')
#win32gui.SetForegroundWindow(hwnd)

time.sleep(3)
count = 0
while True:
    region = findBounds('Mega Man Legacy Collection')
    screenshot = takescreenshot('Mega Man Legacy Collection', region)
    if (screenshot):
        grayimg = screenshot.convert('L')
        pix = grayimg.load()
        val = 0
        for i in range(math.floor(grayimg.width)):
            for j in range(math.floor(grayimg.height)):
                val = val + pix[i,j]
        count = count + 1
        print(count)

        grayimg.save('testscreenshot.png')
