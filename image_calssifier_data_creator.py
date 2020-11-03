from cv2 import cv2
import numpy as np
import glob
import random


'''this code take images and overlaps them to create data to train the visualizer nerual net'''

def overlay_transparent(background, overlay, x_offset, y_offset):
    '''put two images on to of each other with transparnet background on overlay'''

    # get bounding box positions
    y1, y2 = y_offset, y_offset + overlay.shape[0]
    x1, x2 = x_offset, x_offset + overlay.shape[1]
    
    # check to make sure we arnt out of the background somehow
    if x2 > background.shape[1] or y2 > background.shape[0]:
        print("------------FAILED------------")
        return background

    #merege images
    alpha_s = overlay[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    try:
        for c in range(0, 3):
            background[y1:y2, x1:x2, c] = (
                alpha_s * overlay[:, :, c] +
                alpha_l * background[y1:y2, x1:x2, c]
            )
    except:
        print("------------ERROR------------")

    return background





if __name__ == "__main__":
    
    #how many image to to make
    images_to_make = 5000

    # load in background image
    background = (cv2.imread("Background/background-0.png", cv2.IMREAD_UNCHANGED))
    background_main = cv2.cvtColor(background,cv2.COLOR_RGB2RGBA)
    
    #list of images
    image_list = []
    
    #get all the charetcers in the folder
    for filename in glob.glob('characters/*.png'):
        im = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
        im = cv2.cvtColor(im,cv2.COLOR_RGB2RGBA)
        image_list.append(im)

    # data is the final data to save 
    # data = [background image, x bounding box start, y bounding box start, size of bounding box X, size of bounding box Y, type?]
    data = []
    
    starting_value = 0
    for i in range(images_to_make):
        
        #make a copy of the background
        background = background_main.copy()

        #print("X:", rand_x, " Y:", rand_y)

        #get random char from charecters
        image_index = random.randrange(len(image_list))

        # get max x and y value that should be generated
        maxX = background.shape[1] - image_list[image_index].shape[1] - 1
        maxY = background.shape[0] - image_list[image_index].shape[0] - 1

        # get rand values
        rand_x = random.randrange(maxX)
        rand_y = random.randrange(maxY)

        #overlay images and store returned in background
        overlay_transparent(background, image_list[image_index], rand_x, rand_y)
        
        #show image
        #cv2.imshow('image',background)
        #cv2.waitKey(500)
        #cv2.destroyAllWindows()

        # append data
        data.append([background, rand_x, rand_y, image_list[0].shape[1], image_list[0].shape[0], 0]) # clustering vs classification

        # check how long data is 
        if len(data) % 100 == 0:
            print(len(data))
            
            # if 500 data is here save it
            if len(data) % 500 == 0:
                file_name = './visualizer_data/data-{}.npy'.format(starting_value)
                np.save(file_name,data)
                starting_value = starting_value + 1
                data = []




        



    
    


    