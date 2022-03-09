import numpy as np
import cv2
from math import sqrt

# param
# orig_img - grayscale numpy 2D image array
# return
# [(x1,y1),(x2,y2),(x3,y3),(x4,y4)] top-left top-right bottom-left bottom-right
# IS LIST of ARRAYS
def preproc_find_corners(orig_img_gray):
    contours = preproc_find_all_contours(orig_img_gray.copy())
    contours_filtered = preproc_filter_contours(contours)

    four_markers = preproc_find_four_markers(contours_filtered) # is an array of arrays
    
    topleft_corner = four_markers[0][0] #is a numpy array
    topright_corner = four_markers[1][1] #is a numpy array
    bottomright_corner = four_markers[2][2] #is a numpy array
    bottomleft_corner = four_markers[3][3] #is a numpy array
    
    return [topleft_corner, topright_corner, bottomright_corner, bottomleft_corner]

# param img_gray - grayscale numpy 2D image array
# return a LIST of ARRAYs
def preproc_find_all_contours(img_gray):
    img_blur = cv2.GaussianBlur(img_gray,(3,3), sigmaX=0, sigmaY=0)
    edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)
    contours,hierarchy = cv2.findContours(edges, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
    return contours

def preproc_reduce(img_gray,const):
    (height,width) = img_gray.shape
    for i in range(height):
        for j in range(width):
            if(img_gray[i,j]) < const:
                img_gray[i,j] = 0
            else:
                img_gray[i,j] = img_gray[i,j] - const
    return img_gray

# param contours - a LIST of ARRAYS
# return a LIST of ARRAYS
def preproc_filter_contours(contours):
    new_contours = []
    for cnt in contours:
        cnt = cv2.convexHull(cnt)
        epsilon = 0.1 * cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,epsilon,True)
        if len(approx) == 4:
            approx = preproc_sort_rect_points(approx)
       #     if preproc_points_form_parallel(approx):
            new_contours.append(np.array(approx))
    return new_contours

# param
#   cnt_rect- single 4-point contour, NP array
# return [[topleft], [topright], [bottomright], [bottomleft]]
#   LIST of LISTs
def preproc_sort_rect_points(cnt_rect):
    new_cnt_rect = cnt_rect.tolist()
    #sort by increasing y coordinate
    for i in range(len(new_cnt_rect)): #len(cnt_rect) = 4
        for j in range(len(new_cnt_rect) - 1):
            if new_cnt_rect[j][0][1] > new_cnt_rect[j+1][0][1]:
                new_cnt_rect[j],new_cnt_rect[j+1] = new_cnt_rect[j+1],new_cnt_rect[j]

    if new_cnt_rect[0][0][0] > new_cnt_rect[1][0][0]:
        new_cnt_rect[0],new_cnt_rect[1] = new_cnt_rect[1],new_cnt_rect[0]
    if new_cnt_rect[2][0][0] < new_cnt_rect[3][0][0]:
        new_cnt_rect[2],new_cnt_rect[3] = new_cnt_rect[3],new_cnt_rect[2]
    
    return new_cnt_rect

# param cnt_rect - [[topleft], [topright], [bottomright], [bottomleft]]
#   is a LIST of LISTs
# return - True or False
def preproc_points_form_parallel(cnt_rect):
    top_length = sqrt((cnt_rect[0][0][0] - cnt_rect[1][0][0])**2 + (cnt_rect[0][0][1] - cnt_rect[1][0][1])**2)
    bottom_length = sqrt((cnt_rect[2][0][0] - cnt_rect[3][0][0])**2 + (cnt_rect[2][0][1] - cnt_rect[3][0][1])**2)
    left_length = sqrt((cnt_rect[0][0][0] - cnt_rect[3][0][0])**2 + (cnt_rect[0][0][1] - cnt_rect[3][0][1])**2)
    right_length = sqrt((cnt_rect[1][0][0] - cnt_rect[2][0][0])**2 + (cnt_rect[1][0][1] - cnt_rect[2][0][1])**2) 

    if (top_length/bottom_length < 0.9 or top_length/bottom_length > 1.1 or left_length/right_length < 0.9 or left_length/right_length > 1.1):
        return False    
    return True

# param contours_list
#   is a LIST of ARRAYSs
# return [[topleft, topright, bottomright, bottomleft]]
#   is an ARRAY; it is NOT a list
def preproc_find_four_markers(contours_list):
    topleft = contours_list[0].tolist()
    topright = contours_list[0].tolist()
    bottomright = contours_list[0].tolist()
    bottomleft = contours_list[0].tolist()
    #print(topleft[0])

    for cnt in contours_list:
        cnt = cnt.tolist()
        #print(cnt[0])
        if( (cnt[0][0][0] + cnt[0][0][1]) < (topleft[0][0][0] + topleft[0][0][1]) ): #lowest x+y
            topleft = cnt
        if( (cnt[0][0][0] - cnt[0][0][1]) > (topright[0][0][0] - topright[0][0][1]) ): #highest x-y
            topright = cnt
        if( (cnt[0][0][0] + cnt[0][0][1]) > (bottomright[0][0][0] + bottomright[0][0][1]) ): #highest x+y
            bottomright = cnt
        if( (cnt[0][0][0] - cnt[0][0][1]) < (bottomleft[0][0][0] - bottomleft[0][0][1]) ): #lowest x-y
            bottomleft = cnt

    return np.array([topleft, topright, bottomright, bottomleft])

if __name__ == "__main__":
    filename = 'testdata/giap41.jpeg'
    orig_img_color = cv2.imread(filename,cv2.IMREAD_COLOR)
    orig_img_gray = cv2.imread(filename,cv2.IMREAD_GRAYSCALE)
    
    #orig_img_gray = preproc_reduce(orig_img_gray.copy(),10)
    
    four_corners_list = preproc_find_corners(orig_img_gray)
    cv2.drawContours(orig_img_color, four_corners_list, -1, (0,255,0), 10)

    cv2.imwrite('new.jpg',orig_img_color)
