import glob
import os 


f = open('.\\train.txt', 'w')



appened_path = '.\\data\\obj\\'
image_path = '.\\questions\\training\\images\\*'

lines_to_write = [appened_path + str(image.split('\\')[len(image.split('\\'))-1]) + '\n' for image in glob.glob(image_path)]

f.writelines(lines_to_write)

f.close()