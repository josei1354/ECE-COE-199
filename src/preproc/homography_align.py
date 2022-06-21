import cv2
import numpy as np
from math import sqrt
from find_corners import *

# param
#   orig_img_gray is a grayscale 2D numpy image array
#   orig_corners is a LIST of ARRAYS
#   dimension_ref is a LIST with two elements: [a,b]
# return
#   a grayscale 2D numpy image array
def preproc_align_image(orig_img_gray, orig_corners, dimension_ref):
    orig_corners = preproc_find_corners(orig_img_gray)
    new_corners = preproc_solve_new_corners(orig_corners, dimension_ref)
    
    orig_corners_array = np.array(orig_corners)

    #orig_corners_array has a structure
    # [[[55 91]] [[1633 41]] [[1703 2130]] [[  49 2134]]]

    H, mask = cv2.findHomography(orig_corners_array, new_corners)
    img_warp = cv2.warpPerspective(orig_img_gray, H, (orig_img_gray.shape[1],orig_img_gray.shape[0]) )

    new_corners_list = new_corners.tolist()

    """
    img_warp2 = orig_img_gray.copy()
    img_warp2 = cv2.cvtColor(img_warp2,cv2.COLOR_GRAY2RGB)

    cv2.drawContours(img_warp2, np.array([orig_corners]), -1, (0, 255, 0), 10)
    cv2.drawContours(img_warp2, np.array([new_corners]), -1, (255, 0, 0), 10)
    cv2.imwrite("new1.jpg",img_warp2)

    img_warp3 = img_warp.copy()
    img_warp3 = cv2.cvtColor(img_warp3,cv2.COLOR_GRAY2RGB)
    cv2.drawContours(img_warp3, np.array([new_corners]), -1, (255, 0, 0), 10)
    cv2.imwrite("new2.jpg",img_warp3)
    """
    
    img_crop = img_warp[new_corners_list[0][1]:new_corners_list[3][1], new_corners_list[0][0]:new_corners_list[1][0]]

    return img_crop

# param
#   orig_corners is a LIST of ARRAYS [[topleft], [topright], [bottomright], [bottomleft]]
#   dimension_ref is a LIST with two elements: [a,b]
# return
#   is an ARRAY
#   NOTE: this array structure is exampled by
#   [[55 91] [1633 91] [1633 2115] [55 2115]]
#   this structure is different from that of contour lists or the orig_corners_array
def preproc_solve_new_corners(orig_corners, dimension_ref):
    ref_height = dimension_ref[0]
    ref_width = dimension_ref[1]
    ref_ratio = ref_height / ref_width

    orig_topleft = orig_corners[0].tolist()
    orig_topright = orig_corners[1].tolist()
    orig_bottomright = orig_corners[2].tolist()
    orig_bottomleft = orig_corners[3].tolist()

    orig_width = sqrt((orig_topright[0][0] - orig_topleft[0][0])**2 + (orig_topright[0][1] - orig_topleft[0][1])**2)
    orig_height = sqrt((orig_topleft[0][0] - orig_bottomleft[0][0])**2 + (orig_topleft[0][1] - orig_bottomleft[0][1])**2)
    if ref_ratio < (orig_height/orig_width):
        new_width = orig_width
        new_height = new_width * ref_ratio
        
        new_width = int(new_width)
        new_height = int(new_height)
    else:
        new_height = orig_height
        new_width = new_height / ref_ratio

        new_width = int(new_width)
        new_height = int(new_height)

    new_topleft = orig_topleft.copy()[0]
    
    new_topright = new_topleft.copy()
    new_topright[0] = new_topright[0] + new_width
    
    new_bottomright = new_topright.copy()
    new_bottomright[1] = new_bottomright[1] + new_height

    new_bottomleft = new_bottomright.copy()
    new_bottomleft[0] = new_bottomleft[0] - new_width

    return np.array([new_topleft, new_topright, new_bottomright, new_bottomleft])

if __name__ == "__main__":
    from find_corners import *
    import os

    dimension_ref_p1 = [1521,1158]
    dimension_ref_p2 = [1483,1157]
    dimension_ref_p3 = [1480,1162]
    dimension_ref_p4 = [1511,1156]
    
    filename1 = 'samples/sample1.jpg' #page4
    filename2 = 'samples/sample2.jpg' #page2
    filename3 = 'samples/sample3.jpg' #page4
    filename4 = 'samples/sample4.jpg' #page3

    file_used = 'samples/garp1.jpg'
    demension_used = dimension_ref_p1
    
    orig_img_color = cv2.imread(file_used,cv2.IMREAD_COLOR)
    orig_img_gray = cv2.imread(file_used,cv2.IMREAD_GRAYSCALE)

    orig_corners = preproc_find_corners(orig_img_gray)

    img_output_gray = preproc_align_image(orig_img_gray, orig_corners, demension_used)

    img_output_color = cv2.cvtColor(img_output_gray,cv2.COLOR_GRAY2RGB)
    
    cv2.imwrite('new.jpg',img_output_color)
