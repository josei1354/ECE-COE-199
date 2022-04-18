import cv2
import numpy as np
import os
from math import ceil

# param
#   aligned_img_gray is a grayscale 2D numpy image array
#       -- will be the output of preproc_align_image() 
#   page_number is 1,2,3, or 4
# return
#   return True
#   will create a new directory containing appropariately named 3D PNG/JPG images -
#       - of all the individual cropped ROIs
def preproc_roi_output(aligned_img_gray, page_number):

    # EDIT AS NECESSARY
    curr_path = os.getcwd() #curr_path is the same folder where the original picture is
    new_path = os.path.join(curr_path, 'ROI_crops')
    try:
        os.mkdir(new_path)
        print("Created directory", new_path)
    except:
        print("Warning:", new_path, "directory already exists, overwriting files...")
    #cv2.imwrite("ROI_crops/homography_out.png",cv2.cvtColor(aligned_img_gray,cv2.COLOR_GRAY2BGR))

    img = aligned_img_gray

    dimension = img.shape

    height = dimension[0]
    width = dimension[1]
    
    f = open("../" + "ROI_list_page" + str(page_number) + ".txt", "r")
    content = f.readlines()

    for line in content:
        data = line.split()
        topleft_x = ceil(width * float(data[1]))
        topleft_y = ceil(height * float(data[2]))
        bottomright_x = ceil(width * float(data[3]))
        bottomright_y = ceil(height * float(data[4]))

        #print(data[0], topleft_x,topleft_y,bottomright_x,bottomright_y)

        crop_img = img[topleft_y:bottomright_y, topleft_x:bottomright_x]
        cv2.imwrite("ROI_crops/"+data[0]+".png", crop_img)
    
    print("ROI Cropping Complete")
    return True

if __name__ == "__main__":

    dir_of_data = 'blank_forms'
    file_used =  'page1-crop.jpg' #page3
    page_number = 1
    
    curr_dir = os.getcwd()
    os.chdir(os.path.join(curr_dir, dir_of_data))
    #print(os.getcwd())
    
    aligned_img_color = cv2.imread(file_used,cv2.IMREAD_COLOR)
    aligned_img_gray = cv2.imread(file_used,cv2.IMREAD_GRAYSCALE)

    #cv2.imshow(file_used + " - " + str(page_number),aligned_img_gray)

    preproc_roi_output(aligned_img_gray, page_number)
