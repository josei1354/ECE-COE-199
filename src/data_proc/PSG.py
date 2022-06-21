import numpy as np
import cv2

# boundRect is a LIST of TUPLES (tl_x, tl_y, width, height)
# orig_h, orig_w are height and width of original ROI
# params is taken from ROI_types.txt
# 
# return boundRect with the same structure but less possibly items
def psg_filter_labels(boundRect, orig_h, orig_w, params=[]):
    new_boundRect = []
    bot_rect_w = orig_w * params[1]
    bot_rect_h = orig_h * params[0]

    #print("Width and Height: ", bot_rect_w, bot_rect_h)

    for rect in boundRect:
        if rect[0] + rect[2] <= bot_rect_w and rect[1] + rect[3] <= bot_rect_h:
            continue
        else:
            new_boundRect.append(rect)

    return new_boundRect

def psg_binarize_all(img_crops):
    number_of_images = len(img_crops)
    for i in range(number_of_images):
        img = img_crops[i]
        
        T, img2 = cv2.threshold(img,0,255,cv2.THRESH_OTSU)
        
        img3 = 255 - img # white gray text on dark gray background
        img2 = (255-img2) / 255 # 1 for white text 0 for black background

        img4 = img3 * img2 # white text on black background
        
        kernel = np.ones((3,3),np.uint8)
        img4 = cv2.dilate(img4,kernel,iterations = 1)
        img4 = cv2.erode(img4,kernel,iterations = 1)
        
        img4 = 255 - img4

        img_crops.append(img4)

    return img_crops

# params is a list taken from the ROI_types
def psg_crop_all(img_gray, params):
    orig_h, orig_w = img_gray.shape
    boundRect = psg_get_bound_boxes(img_gray)
    boundRect = psg_segment_all(boundRect, orig_h, orig_w)

    #print("All bounds:")
    #for rect in boundRect:
    #    print(rect[1], rect[1]+rect[3], rect[0], rect[0]+rect[2])

    boundRect = psg_filter_labels(boundRect, orig_h, orig_w, params)

    img_crops = []

    for rect in boundRect:
        img_crops.append(img_gray[rect[1]:rect[1]+rect[3],rect[0]:rect[0]+rect[2]])
        #print(rect[1], rect[1]+rect[3], rect[0], rect[0]+rect[2])

    return img_crops

def psg_segment_all(box_list, orig_h, orig_w):
    has_merges = True
    ADD_DIM = 3
    
    for i in range(len(box_list)):
        tl_x,tl_y,new_width,new_height = box_list[i][0],box_list[i][1],box_list[i][2],box_list[i][3]
        
        if ((box_list[i][0] + box_list[i][2]) < (orig_w - ADD_DIM)):
            new_width = box_list[i][2] + ADD_DIM
            
        if ((box_list[i][1] + box_list[i][3]) < (orig_h - ADD_DIM)):
            new_height = box_list[i][3] + ADD_DIM
           
        if box_list[i][0] > ADD_DIM:
            tl_x = box_list[i][0] - ADD_DIM
        else:
            tl_x = 0
            
        if box_list[i][1] > ADD_DIM:
            tl_y = box_list[i][1] - ADD_DIM
        else:
            tl_y = 0
        
        box_list[i] = (tl_x,tl_y,new_width,new_height)

    while(has_merges):
        has_merges = psg_single_merge(box_list, orig_h, orig_w)
    
    return box_list

def psg_single_merge(box_list, orig_h, orig_w):
    for i in range(len(box_list)):
        for j in range(i+1,len(box_list)):
            if psg_boxes_can_merge(box_list[i],box_list[j]):
                new_box = psg_merge_boxes(box_list[i],box_list[j])
                if ((new_box[2]*new_box[3])/(orig_h*orig_w) < 0.9):
                    box_list[i] = new_box
                    box_list.pop(j)
                    return True
    return False

def psg_get_bound_boxes(img_gray):
    height,width = img_gray.shape
    T, img_bin = cv2.threshold(img_gray,0,255,cv2.THRESH_OTSU)
    contours,hierarchy = cv2.findContours(img_bin, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

    boundRect = []

    for cnt in contours:
        rect = cv2.boundingRect(cnt)
        curr_area = rect[2]*rect[3]
        area_allow = False
        
        if curr_area < (height*width*0.5):
            area_allow = True
        box_center_x = rect[0]+(rect[2]/2)
        box_center_y = rect[1]+(rect[3]/2)

        center_of_mass_allow = True
        if ((box_center_x/width) < 0.05):
            center_of_mass_allow = False
        if ((box_center_x/width) > 0.95):
            center_of_mass_allow = False
        if(area_allow and center_of_mass_allow):
            boundRect.append(cv2.boundingRect(cnt))

    return boundRect

def psg_merge_boxes(box1, box2):
    tl_x = min(box1[0],box2[0])
    tl_y = min(box1[1],box2[1])

    br_x = max(box1[0]+box1[2],box2[0]+box2[2])
    br_y = max(box1[1]+box1[3],box2[1]+box2[3])

    new_width = br_x - tl_x
    new_height = br_y - tl_y

    return (tl_x,tl_y,new_width,new_height)

def psg_boxes_can_merge(box1,box2): # boxes are tuples
    area1 = box1[2]*box1[3]
    area2 = box2[2]*box2[3]

    intersect_area = 0
    box_intersect = psg_box_intersection(box1, box2)
    if box_intersect is not None:
        intersect_area = (box_intersect[2]*box_intersect[3])/min(area1,area2)
        if(intersect_area > 0.5):
            return True

    if(box1[1] > box2[1]): #make box1 more up the box2
        box1, box2 = box2, box1

    if(box1[1]+box1[3] < box2[1]):
        return False
    else:
        tl_y = box2[1]
        br_y = min(box1[1]+box1[3],box2[1]+box2[3])
        height_intersect = br_y - tl_y

    intersect_ratio1 = height_intersect/(max(box1[3],box2[3]))
    intersect_ratio2 = height_intersect/(min(box1[3],box2[3]))
    if(intersect_ratio1 > 0.5):
        return True
    if(intersect_ratio1 > 0.3 and intersect_ratio2 > 0.9):
        return True
    
    return False

def psg_box_intersection(box1, box2):
    if(box1[0] > box2[0]): #make box1 more left than box2
        box1, box2 = box2, box1

    if(box1[0]+box1[2] < box2[0]):
        return None
    else:
        tl_x = box2[0]
        br_x = min(box1[0]+box1[2],box2[0]+box2[2])

    if(box1[1] > box2[1]): #make box1 more up the box2
        box1, box2 = box2, box1

    if(box1[1]+box1[3] < box2[1]):
        return None
    else:
        tl_y = box2[1]
        br_y = min(box1[1]+box1[3],box2[1]+box2[3])

    new_width = br_x - tl_x
    new_height = br_y - tl_y

    return(tl_x,tl_y,new_width,new_height)
    

if __name__ == '__main__':

    img = cv2.imread('samples/NameOfHospital.png',flags=cv2.IMREAD_COLOR); #RGB

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    params = []

    #img_crops = psg_crop_all(img_gray, params)
    orig_h, orig_w = img_gray.shape
    boundRect = psg_get_bound_boxes(img_gray)
    boundRect = psg_segment_all(boundRect, orig_h, orig_w)
    
    #img_crops = psg_binarize_all(img_crops)

    #print(len(img_crops))

    #num_img_grays = round(len(img_crops)/2)

    #for i in range(num_img_grays):
        #cv2.imwrite("samples/PSG_OUT_"+str(i)+".png", img_crops[i])
        #cv2.imwrite("samples/PSG_OUT_"+str(i)+"b"+".png", img_crops[i+num_img_grays])
        
    
    #print(len(boundRect))

    #print("Here")

    for i in range(len(boundRect)):
        cv2.rectangle(img, (int(boundRect[i][0]), int(boundRect[i][1])), (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), (0,255,0), 2)

    #box1 = boundRect[9]
    #box2 = boundRect[8]
    #box3 = merge_boxes(box1, box2)
    
    #box4 = box_intersection(box3, box1)

    #print(type(box1))

    #cv2.rectangle(img, (box1[0],box1[1]),(box1[0]+box1[2],box1[1]+box1[3]), (0,255,0), 3)
    #cv2.rectangle(img, (box2[0],box2[1]),(box2[0]+box2[2],box2[1]+box2[3]), (0,255,0), 3)
    #if box4 is not None:
    #    cv2.rectangle(img, (box4[0],box4[1]),(box4[0]+box4[2],box4[1]+box4[3]), (255,0,0), 1)
    #else:
    #    print("No Intersection")

    cv2.imshow('Original', img)
    #cv2.imwrite("samples/PSG_out.png", img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

