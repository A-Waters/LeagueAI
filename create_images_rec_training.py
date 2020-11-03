from screenGrab import grab_screen
import matplotlib as plt
from cv2 import cv2 
import numpy as np
import keyboard
from time import sleep 


'''used speifcily to grab models for image creation off this website https://teemo.gg/model-viewer?skinid=sru_orderminionmelee-0&model-type=creatures 

    use p to puase
    and q to quit
'''



def remove_background(img):
    
    # goes through every pixel and determins if it is close to (162,77,94)
    # if so make it black

    x,y,z = img.shape

    for pixelX in range(x):
        for pixelY in range(y):
            if (color_compare((162,77,94), img[pixelX,pixelY], (20,20,20))):
                img[pixelX,pixelY] = (0,0,0)
            
    return img    

def color_compare(color1, color2, threshold):
    #compares the colors within a threshold
    if (
        (abs(color1[0]-color2[0]) < threshold[0]) and
        (abs(color1[1]-color2[1]) < threshold[1]) and
        (abs(color1[2]-color2[2]) < threshold[2]) ):
        return True
    else: 
        return False


def crop_from_black(img):
    # https://www.nuomiphp.com/eplan/en/155124.html
    # convert to grayscale
    
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # threshold
    thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY)[1]

    # apply close and open morphology to fill tiny black and white holes and save as mask
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # get contours (presumably just one around the nonzero pixels) 
    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    cntr = contours[0]
    x,y,w,h = cv2.boundingRect(cntr)

    # make background transparent by placing the mask into the alpha channel
    new_img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    new_img[:, :, 3] = mask

    # then crop it to bounding rectangle
    crop = new_img[y:y+h, x:x+w]

    return crop

if __name__ == "__main__":
    
    
    paused = True
    #images captured
    captures = []
    
    print("starting paused")
    while True:
        if not paused:
            #capture screen and wait one second
            captures.append(cv2.cvtColor(grab_screen(region=(0,0,1920,1080)),cv2.COLOR_BGR2RGB))
            sleep(1)
             
        # pausing commands
        if keyboard.is_pressed('p'):
            if paused == False:
                paused = True
                print("paused")
                
            else:
                paused = False
                print("resume")
                sleep(1)
                
                for i in range(5):
                    print(i)
                    sleep(1)
                
                print("start")
        
        # quiting command
        if keyboard.is_pressed('q'):
            print("quit")
            break


    print(f"processing {len(captures)}")
    
    # save data
    number = 0
    version = 0

    # loop through images
    for index, capture  in enumerate(captures) :
        
        #% done
        print(f"{index/len(captures) * 100}")
        
        # remove the background image (purple)
        src = remove_background(capture)

    
        # crop the images to the right size
        crop = crop_from_black(src)


        # show images
        #cv2.imshow("image",crop)
        #cv2.waitKey(2)
        #cv2.destroyAllWindows()
    
        # save image
        cv2.imwrite(f'characters/saved{number}-{version}.png', crop)
        number += 1





    
