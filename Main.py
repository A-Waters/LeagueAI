import numpy as np
import win32api
import win32gui
from cv2 import cv2

from screenGrab import grab_screen


if __name__ == "__main__":

    # training_data = np.load("./training_data/training_data-0.npy", allow_pickle=True)
    


    training_data = []
    
    paused = False

    while True:
        if not paused:
            
            MainScreen = grab_screen(region=(0,0,1920,1080))
            # resize to something a bit more acceptable for a CNN
            MainScreen = cv2.resize(MainScreen, (480,270))
            # run a color convert:
            MainScreen = cv2.cvtColor(MainScreen, cv2.COLOR_BGR2RGB)
            # normalize image
            MainScreen = cv2.normalize(MainScreen, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)


            #grab Healthbar
            HealthScreen = grab_screen(region=(550,950,1200,1080))
            HealthScreen = cv2.resize(HealthScreen, (162,32))
            HealthScreen = cv2.cvtColor(HealthScreen, cv2.COLOR_BGR2RGB)
            HealthScreen = cv2.normalize(HealthScreen, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

            #grab minimap
            MiniMapScreen = grab_screen(region=(1640,800,1920,1080))
            MiniMapScreen = cv2.resize(MiniMapScreen, (70,70))
            MiniMapScreen = cv2.cvtColor(MiniMapScreen, cv2.COLOR_BGR2RGB)
            MiniMapScreen = cv2.normalize(MiniMapScreen, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)


            # get mouse pos and if clicked
            flags, hcursor, (x,y) = win32gui.GetCursorInfo()
            mouse_down = 1 if win32api.GetKeyState(0x02) < 0  else 0
            # normalize x and y
            x = x/1920
            y = y/1080


            # get keyboard input for q,w,e,r,d,f
            buttons = [0x51, 0x57, 0x45, 0x52, 0x44, 0x46]
            
            buttons_down = []
            for buttton in buttons:
                buttons_down.append(1 if win32api.GetKeyState(buttton) < 0 else 0)
            

            # create output
            output = [x,y,mouse_down] + buttons_down
            # print((x,y), mouse_down, buttons_down)
            
            training_data.append([MainScreen, HealthScreen, MiniMapScreen, [output]])
            
            # cv2.imshow("screen",MainScreen)

            # save data
            starting_value = 0
            if len(training_data) % 100 == 0:
                print(len(training_data))

                if len(training_data) == 500:
                    file_name = './training_data/training_data-{}.npy'.format(starting_value)
                    np.save(file_name,training_data)
                    print('SAVED')
                    training_data = []
                    starting_value += 1
            
            # quit if hit minus key
            if cv2.waitKey(25) & win32api.GetKeyState(0x6D) < 0:
                print("quit")  
                cv2.destroyAllWindows()
                break

    
