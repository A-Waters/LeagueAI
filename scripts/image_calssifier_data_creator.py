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


    # list of backgrounds
    backgrounds = []

    # load in background images
    for filename in glob.glob('Background/*.png'):
        im = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
        im = cv2.cvtColor(im,cv2.COLOR_RGB2RGBA)
        backgrounds.append(im)

    

    
    #list of charecters
    char_list = []
    
    #get all the charetcers in the folder

    
    for index, folder in enumerate(glob.glob('characters\\*')): 
        print(folder)
        for action in glob.glob(folder+'\\*'):
            print(action)
            for image in glob.glob(action+'\\*.png'):
                im = cv2.imread(image, cv2.IMREAD_UNCHANGED)
                im = cv2.cvtColor(im,cv2.COLOR_RGB2RGBA)
                char_list.append([index,im])




    

    #images to save
    images_to_save = []

    images_char_data = []
    
    images_to_make = 10000
    max_chars = 15
    image_set = 0
    file_num = 0
    type_of_images = 'generated_testing' # 'training' 'generated_testing' or'validation'

    # create images
    for i in range(images_to_make):
        # get number of chars to load up to ten
        charecters_to_make = random.randrange(4,max_chars)

        # get a random background
        random_background = random.choice(backgrounds)

        # get chars to put on image
        char_to_use = []

        for _ in range(charecters_to_make):
            char_to_use.append(random.choice(char_list))


        #make a copy of the background
        background = random_background.copy()


        chars_image_data = []

        for char_index in range(charecters_to_make):
            
            image_of_char = char_to_use[char_index][1]
            index_of_char = char_to_use[char_index][0]

            # scale of char but no more than 0.6 and no less than 0.3
            scale_of_char = random.random()
            scale_of_char = scale_of_char if scale_of_char < 0.6 and scale_of_char > 0.3 else 0.45


            # resize image
            width = int(image_of_char.shape[1] * scale_of_char)
            height = int(image_of_char.shape[0] * scale_of_char) 
            dim = (width, height) 

            image_of_char = cv2.resize(image_of_char, dim, interpolation = cv2.INTER_AREA)  
            
            # where to not place char
            maxX_pos = background.shape[1] - image_of_char.shape[1] - 1
            maxY_pos = background.shape[0] - image_of_char.shape[0] - 1

            # where to place char
            rand_x = random.randrange(maxX_pos)
            rand_y = random.randrange(maxY_pos)

            # overlay images and store returned in background
            overlay_transparent(background, image_of_char, rand_x, rand_y)

            # get center of image for YOLO training
            x_center = (rand_x + image_of_char.shape[1]/2) / background.shape[1]
            y_center = (rand_y + image_of_char.shape[0]/2) / background.shape[0]

            chars_image_data.append([
                                        index_of_char, 
                                        x_center, 
                                        y_center, 
                                        image_of_char.shape[1] / background.shape[1], 
                                        image_of_char.shape[0] / background.shape[0]
                                    ])


        background = cv2.resize(background, (608,608))  

        images_to_save.append(background)
        images_char_data.append(chars_image_data)


        
        if len(images_to_save) % 200 == 0:
            print("Len: ", len(images_to_save))
            
            
            # if 100 data is here save it
            if len(images_to_save) % 1000 == 0:
                
                
                for index,image in enumerate(images_to_save):
                    file_name = f'./questions/{type_of_images}/images/image-{image_set}-{file_num}.jpg'
                    
                    cv2.imwrite(file_name, image)


                    file_name = f'./questions/{type_of_images}/data/data-{image_set}-{file_num}.txt'


                    with open(file_name, 'w') as f:
                        for item in images_char_data[index]:
                            if item[0] == -1:
                                print("NEGATIVE 1 FOUND AT FILE: ", file_num)
                            item = [str(int) for int in item]
                            item = " ".join(item)
                            f.write("%s\n" % item)

                    file_num = file_num + 1

                print(file_num/images_to_make)
                images_to_save = []
                images_char_data = []
                



        '''
        cv2.imshow('image',background)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        '''

    '''


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
        


    '''

        



    
    


    