from cv2 import cv2
import numpy as np
import glob
import random




def overlay_transparent(background, overlay, x_offset, y_offset):

    y1, y2 = y_offset, y_offset + overlay.shape[0]
    x1, x2 = x_offset, x_offset + overlay.shape[1]

    # print("start: ", (x1,y1), "End: ", (x2,y2))
    
    if x2 > background.shape[1] or y2 > background.shape[0]:
        print("------------FAILED------------")
        return background


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
    

    images_to_make = 5000

    background = (cv2.imread("Background/background-0.png", cv2.IMREAD_UNCHANGED))
    background_main = cv2.cvtColor(background,cv2.COLOR_RGB2RGBA)
    
    image_list = []
    
    for filename in glob.glob('characters/*.png'):
        im = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
        im = cv2.cvtColor(im,cv2.COLOR_RGB2RGBA)
        image_list.append(im)


    data = []
    
    starting_value = 0
    for i in range(images_to_make):

        background = background_main.copy()






        #print("X:", rand_x, " Y:", rand_y)

        image_index = random.randrange(len(image_list))

        maxX = background.shape[1] - image_list[image_index].shape[1] - 1
        maxY = background.shape[0] - image_list[image_index].shape[0] - 1

        rand_x = random.randrange(maxX)
        rand_y = random.randrange(maxY)

        overlay_transparent(background, image_list[image_index], rand_x, rand_y)
        
        #cv2.imshow('image',background)
        #cv2.waitKey(500)
        #cv2.destroyAllWindows()


        data.append([background, rand_x, rand_y, image_list[0].shape[1], image_list[0].shape[0]])

        
        if len(data) % 100 == 0:
            print(len(data))

            if len(data) % 500 == 0:
                file_name = './visualizer_data/data-{}.npy'.format(starting_value)
                np.save(file_name,data)
                starting_value = starting_value + 1
                data = []




        



    
    


    