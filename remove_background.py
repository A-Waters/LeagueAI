from cv2 import cv2
import glob
import numpy as np
import os

#list of charecters
char_list = []

#get all the charetcers in the folder


for folder in glob.glob('characters\\*'): 
    print(folder)
    for action in glob.glob(folder+'\\*'):
        print(action)
        for image_path in glob.glob(action+'\\*.jpg'):
            im = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
            im = cv2.cvtColor(im,cv2.COLOR_RGB2RGBA)

            
            for row_index, row_value in enumerate(im):
                for pixel_index, pixel_value in enumerate(row_value):
                    r,g,b,a = pixel_value
                    if not np.count_nonzero([r,g,b]) > 0 :
                        #print("found", pixel_value)
                        pixel_value = (0,0,0,0)
                        #print("resulting", pixel_value)

                        im[row_index, pixel_index] = pixel_value
            
            os.remove(image_path)
            image_path = image_path.split('.')
            print(image_path[0]+'.PNG')
            cv2.imwrite(image_path[0]+'.PNG', im)