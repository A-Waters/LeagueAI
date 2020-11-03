from screenGrab import grab_screen
from cv2 import cv2 
from time import sleep 
import numpy as np


'''this code take your main screens montitor every 3 seconds and save it in Backgrounds'''



if __name__ == "__main__":
    num = 0
    while True:

        MainScreen = grab_screen(region=(0,0,1920,1080))
        MainScreen = cv2.cvtColor(MainScreen, cv2.COLOR_BGR2RGB)
        print("captured")

        sleep(3)
        #cv2.imshow('capture',MainScreen)
        

        cv2.imwrite(f"./Background/background-{num}.png",MainScreen)
        num = num + 1

