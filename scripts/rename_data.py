import glob
import os

data_path = '.\\questions\\generated_testing\\data\\*'
for data_path in glob.glob(data_path):
    
    print(data_path)
    
    new_path = '\\'.join(data_path.split('\\')[:len(data_path.split('\\'))-1])

    new_name = '\\image-' + '-'.join(data_path.split('-')[1:len(data_path.split('-'))])

    new_file = new_path+new_name
    os.rename(data_path,new_file)
    
