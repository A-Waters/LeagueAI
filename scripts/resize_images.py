import glob
from cv2 import cv2

image_path = '.\\questions\\generated_testing\\images\\*'
for image_path in glob.glob(image_path):
    print(image_path)
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    image = cv2.resize(image, (480,480))

    cv2.imwrite(image_path,image)
