import cv2
import numpy as np
import os
from find_corners import *
from homography_align import *
from roi_cropping import *


# param
#   filename is the path of the originally scanned image
#   page_number is 1,2,3, or 4
# return
#   return True
#   will create a new image file - the homography_aligned 3D image
#   will also create a new directory containin all the individual cropped ROIs
def preproc_main(filename, page_number):
    #print(filename)
    #print(page_number)

    dimension_ref = ([1,1],[1521,1158], [1483,1157], [1480,1162], [1511,1156])
    
    dimension_used = dimension_ref[page_number]

    # FIX
    aligned_filename = 'homography_out.png'

    orig_img_color = cv2.imread(filename,cv2.IMREAD_COLOR)
    orig_img_gray = cv2.imread(filename,cv2.IMREAD_GRAYSCALE)

    print("Finding corners...")
    orig_corners = preproc_find_corners(orig_img_gray)

    print("Performing Homography Alignment...")
    img_homo_aligned_gray = preproc_align_image(orig_img_gray, orig_corners, dimension_used)
    img_homo_aligned_color = cv2.cvtColor(img_homo_aligned_gray,cv2.COLOR_GRAY2RGB)

    cv2.imwrite('ROI_crops/' + aligned_filename,img_homo_aligned_color)
    print("Alignment Successful")
    
    print("Cropping ROIs...")
    preproc_roi_output(img_homo_aligned_gray,page_number)

    print("Preprossing Complete")
    return True

if __name__ == "__main__":
    from find_corners import *
    from homography_align import *
    from roi_cropping import *
    
    import argparse

    #filename =  'samples/samplex2.jpg' #page1
    #page_number = 1

    parser = argparse.ArgumentParser()

    parser.add_argument("--filename", type=str,required=True)
    parser.add_argument("--pagenum", type=int,required=True)
    args = parser.parse_args()

    filename = args.filename
    page_number = args.pagenum

    curr_dir = os.getcwd()
    new_dir=curr_dir

    while True:
        if filename[:3] == "../" or filename[:3]== "..\\":
            filename = filename[3:]
            new_dir = os.path.dirname(new_dir)
        else:
            break

    os.chdir(new_dir)

    #print(os.getcwd())

    if filename[:11] == "data_actual":
        new_dir = os.path.join(new_dir, "data_actual")
        filename = filename[12:]
        pagefolder = filename[:5]
        new_dir = os.path.join(new_dir, pagefolder)
        filename = filename[6:]
        os.chdir(new_dir)
    #print(filename)
    #print(os.getcwd())
    #at this point, filename is "directory/filename.png" or just "filename.png"

    if(filename.find("/") > 0):
        temp = filename.find("/")
        new_dir = os.path.join(new_dir,filename[:temp])
        os.chdir(new_dir)
        filename = filename[(temp+1):]

    #print(filename)
    #print(os.getcwd())

    #at this point. filename is just "filename.png" and that file is in the same working directory

    preproc_main(filename, page_number)
