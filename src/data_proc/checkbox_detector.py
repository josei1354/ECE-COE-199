import numpy as np
import cv2

# param img_gray - graysscale numpy 2D image array
#    return_search_area - bool, set to true only for debugging
# return True or False, numpy_image_array
def checkbox_main_detec(img_gray, return_search_area):
    img_gray = img_gray.copy()
    contours_list = checkbox_find_all_contours(img_gray)
    largest_cnt = checkbox_get_largest_contour(contours_list)
    img_binary = checkbox_binarize(img_gray)

    img_crop, search_area_3d = checkbox_crop(img_binary,largest_cnt)
    cv2.drawContours(search_area_3d, [largest_cnt], -1, (0,255,0), 1)

    has_check = checkbox_img_has_black(img_crop)

    if(return_search_area):
        return has_check, search_area_3d
    else:
        return has_check

# param img_binary - graysscale numpy 2D image array
# return True or False
def checkbox_img_has_black(img_binary):
    h = img_binary.shape[0]
    w = img_binary.shape[1]

    for y in range(0,h):
        for x in range(0,w):
            if (img_binary[y,x] == 0):
                return True
    return False

def checkbox_binarize(img_gray):
    T, img_binary = cv2.threshold(img_gray,0,255,cv2.THRESH_OTSU)
    return img_binary

# param img_gray - grayscale numpy 2D image array
# return a LIST of ARRAYs
def checkbox_find_all_contours(img_gray):
    img_gray = checkbox_binarize(img_gray)
    img_blur = cv2.GaussianBlur(img_gray,(3,3), sigmaX=0, sigmaY=0)
    edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)
    contours,hierarchy = cv2.findContours(edges, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
    return contours

# param contours - a LIST of ARRAYS
# return a single contour
def checkbox_get_largest_contour(contours):
    largest_area = 0
    
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        curr_area = w*h
        if(curr_area) > largest_area:
            largest_area = curr_area
            largest_cnt = cnt
    return largest_cnt

def checkbox_crop(img_binary,cnt):
    img_binary_copy = img_binary.copy()

    x,y,w,h = cv2.boundingRect(cnt)
    LR_INDENT = 0.25 # set between 0 and 0.5
    TB_INDENT = 0.25 # larger value = smaller rectangle

    tl_y = int(y + h*(LR_INDENT))
    br_y = int(y + h*(1-LR_INDENT))
    tl_x = int(x + w*(TB_INDENT))
    br_x = int(x + w*(1-TB_INDENT))

    img_crop = img_binary_copy[tl_y:br_y, tl_x:br_x]
    
    search_area_3d = cv2.cvtColor(img_binary_copy,cv2.COLOR_GRAY2RGB)
    cv2.rectangle(search_area_3d, (tl_x,tl_y), (br_x,br_y) ,(255,0,0), 1)

    return img_crop, search_area_3d

if __name__ == "__main__":
    filename = 'samples/Female.png'
    orig_img_color = cv2.imread(filename,cv2.IMREAD_COLOR)
    orig_img_gray = cv2.imread(filename,cv2.IMREAD_GRAYSCALE)

    return_search_area = True
    is_checked, img_search = checkbox_main_detec(orig_img_gray, return_search_area)

    print(is_checked)
    cv2.imshow('Warped', img_search)

    
