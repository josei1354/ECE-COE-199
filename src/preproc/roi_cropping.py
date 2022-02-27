import cv2
import numpy as np
import os

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
    cv2.imwrite("ROI_crops/homography_out.png",cv2.cvtColor(aligned_img_gray,cv2.COLOR_GRAY2BGR))

    f = open("../" + "ROI_list_page" + str(page_number) + ".txt", "r")
    print(f.read())

    print("here")
    return True

if __name__ == "__main__": 

    file_used =  'samples/samplex2_out.png' #page1
    page_number = 1
    
    aligned_img_color = cv2.imread(file_used,cv2.IMREAD_COLOR)
    aligned_img_gray = cv2.imread(file_used,cv2.IMREAD_GRAYSCALE)

    #cv2.imshow(file_used + " - " + str(page_number),aligned_img_gray)

    preproc_roi_output(aligned_img_gray, page_number)
