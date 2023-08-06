import cv2
import numpy as np


sift = cv2.SIFT_create()

def sift_sim(img1, img2, algorithm='SIFT'):
    # Converting to grayscale and resizing
    
    #i1 = cv2.resize(cv2.imread(img1, cv2.IMREAD_GRAYSCALE), SIM_IMAGE_SIZE)
    #i2 = cv2.resize(cv2.imread(img2, cv2.IMREAD_GRAYSCALE), SIM_IMAGE_SIZE)
    i1 = img1
    i2 = img2
    SIFT_RATIO = 0.9

    similarity = 0.0

    if algorithm == 'SIFT':
        # Using OpenCV for feature detection and matching
        
        #sift = cv2.SIFT_create()
        
        k1, d1 = sift.detectAndCompute(i1, None)
        k2, d2 = sift.detectAndCompute(i2, None)

        bf = cv2.BFMatcher()
        matches = bf.knnMatch(d1, d2, k=2)

        for m, n in matches:
            if m.distance < SIFT_RATIO * n.distance:
                similarity += 1.0

        # Custom normalization for better variance in the similarity matrix
        if similarity == len(matches):
            similarity = 1.0
        elif similarity > 1.0:
            similarity = 1.0 - 1.0/similarity
        elif similarity == 1.0:
            similarity = 0.1
        else:
            similarity = 0.0

    #print("got sift similarity ",similarity)
    return similarity




def hist_sim(img1,img2):
    ph1 = patch_histogram(img1)
    ph2 = patch_histogram(img2)
    diff = np.mean(np.abs(ph2-ph1)) 
    #higher values should mean more similarity
    return 1.0-diff