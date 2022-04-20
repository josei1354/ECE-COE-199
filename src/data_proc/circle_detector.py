import numpy as np
import cv2
from math import sqrt

# param img_gray - graysscale numpy 2D image array
#    return_search_area - bool, set to true only for debugging
# return True or False, numpy_image_array
def encircle_main_detec(img_gray, return_search_area, min_area, max_area):
    img_gray = img_gray.copy()
    contours_list = encircle_find_all_contours(img_gray)

    orig_height = img_gray.shape[0]
    orig_width = img_gray.shape[1]
    contours_filtered = encircle_filter_contours_by_center(contours_list, orig_height, orig_width)
    
    largest_cnt = encircle_get_largest_contour(contours_filtered)

    img_gray = cv2.cvtColor(img_gray,cv2.COLOR_GRAY2RGB)
    cv2.drawContours(img_gray, [largest_cnt], -1, (0,255,0), 1)

    has_circle = encircle_check_area(largest_cnt, min_area, max_area, orig_height*orig_width, return_search_area)

    if(return_search_area):
        return has_circle, img_gray
    else:
        return has_circle

def encircle_binarize(img_gray):
    T, img_binary = cv2.threshold(img_gray,0,255,cv2.THRESH_OTSU)
    return img_binary

# param img_gray - grayscale numpy 2D image array
# return a LIST of ARRAYs
def encircle_find_all_contours(img_gray):
    img_gray = encircle_binarize(img_gray)
    img_blur = cv2.GaussianBlur(img_gray,(3,3), sigmaX=0, sigmaY=0)
    edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)
    contours,hierarchy = cv2.findContours(edges, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
    return contours

def encircle_filter_contours_by_center(contours, orig_height, orig_width):
    contours_filtered = []
    radius = min(orig_height, orig_width) / 3
    
    img_x = orig_width / 2
    img_y = orig_height / 2

    for cnt in contours:
        cnt = cv2.convexHull(cnt)
        M = cv2.moments(cnt)
        if(M["m00"] == 0):
            continue
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        dist = (cX - img_x)**2 + (cY - img_y)**2
        dist = sqrt(dist)
        if(dist < radius):
            contours_filtered.append(cnt)

    return contours_filtered

def encircle_check_area(cnt, min_area, max_area, orig_area, print_ratio):
    cnt_area = cv2.contourArea(cnt)
    area_ratio = cnt_area / orig_area
    if(print_ratio):
        print("Ratio: ",area_ratio)
    if((max_area < area_ratio) or (min_area > area_ratio)):
        return False
    else:
        return True

# param contours - a LIST of ARRAYS
# return a LIST of ARRAYS
def encircle_get_largest_contour(contours):
    largest_area = 0
    
    for cnt in contours:
        cnt = cv2.convexHull(cnt)
        curr_area = cv2.contourArea(cnt)
        if curr_area > largest_area:
            largest_area = curr_area
            largest_cnt = cnt
    return largest_cnt


if __name__ == "__main__":
    filename = 'samples/TimePM.png'
    orig_img_color = cv2.imread(filename,cv2.IMREAD_COLOR)
    orig_img_gray = cv2.imread(filename,cv2.IMREAD_GRAYSCALE)

    return_largest_cnt = True
    has_circle, img_search = encircle_main_detec(orig_img_gray, return_largest_cnt, 0.1, 1)
    print(has_circle)
    
    cv2.imshow('Warped', img_search)

    
