import numpy as np
import win32api
import win32gui
from time import sleep
from cv2 import cv2

from screenGrab import grab_screen


starting_value = 0 

while True:
    sleep(1)
    MainScreen = grab_screen(region=(0,0,1920,1080))
    # resize to something a bit more acceptable for a CNN
    MainScreen = cv2.resize(MainScreen, (480,480))
    # run a color convert:
    MainScreen = cv2.cvtColor(MainScreen, cv2.COLOR_BGR2RGB)


    file_name = './questions/real_test/training_data-{}.jpg'.format(starting_value)
    cv2.imwrite(file_name, MainScreen)
    starting_value += 1