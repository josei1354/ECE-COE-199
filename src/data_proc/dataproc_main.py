import cv2
import numpy as np
import os
from checkbox_detector import *
from circle_detector import *

# param
#   filename is the path of the originally scanned image
#   page_number is 1,2,3, or 4
# return
#   return dict of ROIs
def dataproc_main(page_number):
    #print(page_number)

    print("Processing ROIs...")

    output_dict = {}

    f = open("../" + "ROI_types_page" + str(page_number) + ".txt")
    content = f.readlines()

    for line in content:
        data = line.split()
        roi_img = cv2.imread("ROI_crops/"+data[0]+".png",cv2.IMREAD_GRAYSCALE)
        
        if(data[1] == "EN"):
            has_circle = encircle_main_detec(roi_img, False, float(data[2]), float(data[3]))
            output_dict[data[0]] = ["Encirclement",has_circle]
        elif(data[1] == "CB"):
            has_check = checkbox_main_detec(roi_img, False)
            output_dict[data[0]] = ["Checkbox",has_check]
        elif(data[1] == "TX"):
            output_dict[data[0]] = ["Text", "None Yet"]

    f.close()

    print("Processing Complete")
    
    return output_dict
            

if __name__ == "__main__":
    print("Hello")
