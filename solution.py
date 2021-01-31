import numpy as np
import cv2
import math
def find(star_img,crop_img):                  

    star_row=star_img.shape[0] #get the number of rows of the star image
    star_col=star_img.shape[1] #get the number of columns of the star image
    crop_row=crop_img.shape[0] #get the number of the rows of the crop image
    crop_col=crop_img.shape[1] #get the number of columns of the crop image
    surf = cv2.xfeatures2d.SURF_create(400) #define the surf algorithm's object
    bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=False)  #define the brute force matcher algorithm         
    keypoints2, des2 = surf.detectAndCompute(crop_img,None) #detect and extract the keypoints of the crop image
    keypoints1, des1 = surf.detectAndCompute(star_img,None) #detect and extract the keypoints of the star image scene
    h,w=crop_img.shape[0],crop_img.shape[1] #get the number of rows and columns of the crop image
    matches=bf.match(des2,des1)  #match the descriptors of the crop image with the descriptors of the star image  
    max_matches=-math.inf #define and assign the max_matches to -infinity
    corner_x,corner_y,width,height=-1,-1,-1,-1 #define and assign the answers cornerx and cornery of the template crop in the star scene to -1
    for i in range(star_row):
        for j in range(star_col): # sliding over the star scene in order to find the corners of the template crop image
            if i+crop_row<=star_row and j+crop_col<=star_col: #check if the current window in the scene matches the dimensions of the crop image
               star_window=star_img[i:i+crop_row,j:j+crop_col] #get the current window in the star scene
               matches_number=0 #define and assign the current number of matched keypoints between the current window in scene and the crop image to zero
               for i in range(len(matches)): # loop over the matches keypoints between the scene and the crop image
                   if keypoints1[matches[i].trainIdx].pt[0]<=j+w and keypoints1[matches[i].trainIdx].pt[1]<=i+h and keypoints1[matches[i].trainIdx].pt[1]>=i and keypoints1[matches[i].trainIdx].pt[0]>=j:  #check if the current matched keypoint in the scene is located in the current window of the scene
                       matches_number+=1 # if yes, then count it
               if max_matches<matches_number:# check if the current window of the scene has a greater number of keypoints matches
                  corner_x,corner_y=i,j # if yes, then make the max_matches variable the maximum number of matches and get the current corners of the current window of the scene
                  max_matches=matches_number
                  
    return corner_x,corner_y #return the corners of the window in scene that has a maximum number of keypoints matches between the window of the scene and the crop image
star_img=cv2.imread('StarMap.png',0) #read the star image and convert it to grayscale
crop_img=cv2.imread('Small_area.png',0)
corner_x,corner_y=find(star_img,crop_img)
width,height=crop.shape[1],crop.shape[0]
cv2.imshow(crop) #show the template crop image
cv2.imshow(star[corner_x:corner_x+height,corner_y:corner_y+width]) #show the window in the scene that matches the crop image
