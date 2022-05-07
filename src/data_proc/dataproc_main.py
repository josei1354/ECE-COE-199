import cv2
import numpy as np
import os
#from pytess_detector import *
from checkbox_detector import *
from circle_detector import *
from PSG import *
#import pytesseract

# param
#   filename is the path of the originally scanned image
#   page_number is 1,2,3, or 4
# return
#   return dict of ROIs
def dataproc_main(page_number):

#    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    print("Processing ROIs...")

    output_dict = {}

    f = open("../" + "ROI_types_page" + str(page_number) + ".txt")
    content = f.readlines()

    for line in content:
        data = line.strip().split()
        #print(data)
        if(len(data) == 0):
            continue

        image_path = data[0] + ".png"
        debug_mode=False
        
        roi_img = cv2.imread("ROI_crops/"+image_path,cv2.IMREAD_GRAYSCALE)
        if(roi_img is None):
            continue
        
        if(data[1] == "EN"):
            has_circle = encircle_main_detec(roi_img, debug_mode, float(data[2]), float(data[3]))
            output_dict[data[0]] = ["Encirclement",has_circle]
        elif(data[1] == "CB"):
            has_check = checkbox_main_detec(roi_img, debug_mode)
            output_dict[data[0]] = ["Checkbox",has_check]
        elif(data[1] == "TX"):
            # to complete
            # from data[2] onwards
            params = [] 
            
            img_crops = psg_crop_all(roi_img, params)
            img_crops = psg_binarize_all(img_crops)
            num_img_grays = round(len(img_crops)/2)

            for i in range(num_img_grays):
                cv2.imwrite("ROI_crops/"+data[0]+str(i+1)+".png", img_crops[i])
                cv2.imwrite("ROI_crops/"+data[0]+str(i+1)+"b"+".png", img_crops[i+num_img_grays])
            
            output_dict[data[0]] = ["TX", "None Yet"]

        elif(data[1] == "TESS"):
#            pytess_out = pytess_detec(roi_img, digits_only=True, debug_mode=False)
            output_dict[data[0]] = ["TESS", "None Yet"]
        else:
            print("Error in ROI_types_page.txt")

    f.close()

    print("Processing Complete")
    
    return output_dict
            

if __name__ == "__main__":
    print("Hello")
