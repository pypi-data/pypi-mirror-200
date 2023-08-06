import cv2 
import numpy as np
import math
from matplotlib import pyplot as plt
import copy
from skimage.metrics import structural_similarity as ssim
#from skimage.metrics import normalized_mutual_information as nmi #-- takes a lot of time
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import normalized_root_mse as nrmse

from skimage.filters.rank import median
from skimage.morphology import disk, ball

from scipy import ndimage
from image_comparisons import sift_sim, hist_sim

import time

def extract_neighborhood_patch_proposals(img, template, box, variance, stride):
    patches = []
    locs = []

    x_start = (box[0]-variance[0]) 
    x_end = (box[0]+variance[0])

    y_start = (box[1]-variance[1])
    y_end = (box[1]+variance[1])

    print("y start, variance ",y_start, variance, box)

    #make sure the boxes are not suggested outside the image range
    if x_start<0:
        x_start=0
    if x_end>img.shape[0]:
        x_end=img.shape[0]
    if y_start<0:
        y_start=0
    if y_end>img.shape[1]:
        y_end = img.shape[1]

    for i in range(x_start, x_end, stride[0]):
        for j in range(y_start, y_end, stride[1]):
            
            patches.append(img[i:i+template.shape[0], j:j+template.shape[1]])
            
            #cv2.imshow("patch ",patches[-1])

            locs.append([i,j, i+template.shape[0], j+template.shape[1]])
    return patches,locs

def nested_regions(template, proposal, subsizes ):
    #print("got subsizes in nested_regions ",subsizes)
    h,w = template.shape[0], template.shape[1]
    pairs = [[template,proposal]]
    for s in subsizes:
        
        if s[0]>=1: #corresponds to the hypothesis that the camera has moved forward leading to a zooming effect on the tracking region
            hs,ws = int(float(h/s[0])), int(float(w/s[1]))
            p = proposal[int((h-hs)/2.0): h-int((h-hs)/2.0), int((w-ws)/2.0): w-int((w-ws)/2.0)]
            
            p = cv2.resize(p, (w,h))
            
            pairs.append([template,p])

        else:
            t = template[int(h*s[0]):, int(w*s[1]): ]
            p = proposal[int(h*s[0]):, int(w*s[1]): ]
            pairs.append([t,p])
    return pairs



def sliding_window_metrics(template, proposals, nested_region_subsizes, comparison_functions):
    fmetrics_all = [[] for _ in comparison_functions]

    patches = proposals
    resize_suggestions = []

    n_comparisons = 0

    for p in range(len(patches)):

        templates_proposals_pairs = nested_regions(template, patches[p], nested_region_subsizes)

        fmetrics = [[] for _ in comparison_functions]

        for n in templates_proposals_pairs:
            

            for f in range(len(comparison_functions)):
                func = comparison_functions[f]
                #t1 = time.time()
                fmetrics[f].append(func(n[0],n[1]))
                #t2 = time.time()
                #print("time taken by comparison_functions ",t2-t1)
            n_comparisons+=1

        resize_suggestion = np.argmax(fmetrics[0])
        resize_suggestions.append(resize_suggestion)
        
        

        fmetrics = [np.sum(f)/len(templates_proposals_pairs) for f in fmetrics]
        
        for f in range(len(comparison_functions)):
            fmetrics_all[f].append( fmetrics[f] )

    fmetrics_all = [np.array(f)/np.max(f) for f in fmetrics_all]
    print("total number of pairwise image comparisons ",n_comparisons)
    print("size of patch comparison ",patches[0].shape)
    metric_scores = np.sum(fmetrics_all,axis=0)/len(comparison_functions)
    return metric_scores, np.bincount(resize_suggestions).argmax()







def coarse_center_adjustment(bboxes, cX, cY, res, bound_value):
    
    x_shift = -(res.shape[1]//2 - cX)
    y_shift = -(res.shape[0]//2 - cY)
    #print("x_shift y shift ",x_shift, y_shift)

    
    for n in range(3):
        h,w = bboxes[n][2]-bboxes[n][0], bboxes[n][3]-bboxes[n][1]
        #print("h,w ",h,w)

        bboxes[n][0] = bound_value( bboxes[n][0]+y_shift, 0 )
        bboxes[n][1] = bound_value( bboxes[n][1]+x_shift, 1 )
        bboxes[n][2] = bound_value( bboxes[n][2]+y_shift, 0 )
        bboxes[n][3] = bound_value( bboxes[n][3]+x_shift, 1 )
    

    return bboxes

def fine_center_adjustment(location,bboxes):
    center_coordinates_f = (  int(0.5*(location[1]+location[3] )) , int(0.5*(location[0]+location[2]))   )

    center_coordinates_c = (  int(0.5*(bboxes[1][1]+bboxes[1][3] )) , int(0.5*(bboxes[1][0]+bboxes[1][2]))   )

    dx = center_coordinates_c[0] - center_coordinates_f[0]
    dy = center_coordinates_c[1] - center_coordinates_f[1]

    
    bboxes[0][0] = max(0, bboxes[0][0] - dy )
    bboxes[0][1] = max(0, bboxes[0][1] - dx )
    bboxes[0][2] = max(0, bboxes[0][2] - dy )
    bboxes[0][3] = max(0, bboxes[0][3] - dx )

    bboxes[1][0] = max(0, bboxes[1][0] - dy )
    bboxes[1][1] = max(0, bboxes[1][1] - dx )
    bboxes[1][2] = max(0, bboxes[1][2] - dy )
    bboxes[1][3] = max(0, bboxes[1][3] - dx )


    bboxes[2][0] = max(0, bboxes[2][0] - dy )
    bboxes[2][1] = max(0, bboxes[2][1] - dx )
    bboxes[2][2] = max(0, bboxes[2][2] - dy )
    bboxes[2][3] = max(0, bboxes[2][3] - dx )

    return bboxes

def patch_histogram(patch):
    #patch max if around 255
    intensity_hist = cv2.calcHist([patch],[0],None, [360],[0,360]) # histogram of 256 bins
    #cv2.normalize(intensity_hist, intensity_hist, 0,256, cv2.NORM_MINMAX)

    patch = np.float32(patch)/255.0
    gx = cv2.Sobel(patch, cv2.CV_32F, 1, 0, ksize=1)
    gy = cv2.Sobel(patch, cv2.CV_32F, 0, 1, ksize=1)
    mag, angle = cv2.cartToPolar(gx,gy, angleInDegrees=True)
    angle_hist = cv2.calcHist([angle],[0],None, [360],[0,360])
    mag_hist = cv2.calcHist([mag],[0],None, [360],[0,360])
    #cv2.normalize(angle_hist, angle_hist, 0,256, cv2.NORM_MINMAX)
    #cv2.normalize(mag_hist, mag_hist, 0,256, cv2.NORM_MINMAX)

    #return intensity_hist.flatten()
    return np.stack([intensity_hist.flatten(),angle_hist.flatten(), mag_hist.flatten()])



def check_increase_size(image, bboxes, big_patch):
    #algorithm to autodetect increase in size of objects.. not working well 
    image_region = image[bboxes[1][0]:bboxes[1][2], bboxes[1][1]:bboxes[1][3] ]
    ph1 = patch_histogram(big_patch)
    ph2 = patch_histogram(image_region)
    start_res = np.mean(np.abs(ph2-ph1))

    #start_res = np.max(res)
    size_inc = [0,0]
    exit_loop = False
    #try maximum 10 times
    for _ in range(10):
        

        size_options = [ [1+size_inc[0],size_inc[1]],   
                        [size_inc[0],1+size_inc[1]], 
                        [1+size_inc[0],1+size_inc[1]],  
                        [size_inc[0]-1,size_inc[1]] ,  
                        [size_inc[0],size_inc[1]-1] ,  
                        [size_inc[0]-1,size_inc[1]-1]  ]
        nrs = []

        

        for n in range(3):
            image_region = image[bboxes[1][0]-size_options[n][0]:bboxes[1][2]+size_options[n][0], bboxes[1][1]-size_options[n][1]:bboxes[1][3]+size_options[n][1] ]
            
            #rbpatch = cv2.resize(big_patch, (big_patch.shape[0] + size_options[n][0], big_patch.shape[1]+size_options[n][1]))
            rbpatch = big_patch

            #image_region = cv2.resize(image_region, (image_region.shape[0] + size_options[n][0], image_region.shape[1]+size_options[n][1]))
            #print("shapes ",image_region.shape, rbpatch.shape)
            
            if image_region.shape[0] < rbpatch.shape[0] or image_region.shape[1]<rbpatch.shape[1] :
                print("cannot increase size anymore ")
                exit_loop = True
            else:
                ph2 = patch_histogram(image_region)
                res = np.mean(np.abs(ph2-ph1)) 

                nrs.append(res)

            

        if start_res<all(nrs):
            print("optimization did not suggest size increase ")
            break
        elif exit_loop:
            print("cannot increase size anymore ")
            break
        else:
            size_opt = size_options[np.argmin(nrs)]
            size_inc[0] =size_opt[0]
            size_inc[1] =size_opt[1]
            start_res = np.argmin(nrs)
            print("increasing size to ",size_inc)

    print("coarse adjustment suggested size increase ",size_inc)

    for k in range(3): #trmplate matching box, ssim matching box and the user defined box
        bboxes[k][2] = min(image.shape[0], int(bboxes[k][2] + size_inc[0]/2       ) )
        bboxes[k][0] = max(0, int(bboxes[k][0] - size_inc[0]/2         ) )

        bboxes[k][3] = min(image.shape[1], int(bboxes[k][3] + size_inc[1]/2   ) )
        bboxes[k][1] = max(0,int(bboxes[k][1] - size_inc[1]/2     ) )

    return bboxes




def coarse_adjustment(image, bboxes, big_patch, big_variance, bound_value):
    #big_variance = adjust_variance(bboxes,big_variance,image)
    
    y_start = bound_value (bboxes[1][0]-big_variance[0], 0)
    y_end = bound_value( bboxes[1][2]+big_variance[0],0)

    x_start = bound_value(bboxes[1][1]-big_variance[1], 1)
    x_end = bound_value(bboxes[1][3]+big_variance[1], 1)



    image_region = image[y_start:y_end, x_start:x_end ]
    





    res = cv2.matchTemplate( image_region  ,big_patch, cv2.TM_CCOEFF_NORMED)

    
    res[res<np.mean(res)]= min(1.0, np.min(res))
    res = res-(np.min(res)*np.ones_like(res)) 
    res = res/max(1.0,np.max(res))

    res[res<0.9*np.max(res)]=0


    cv2.imshow("res",res)

    M = cv2.moments(res)
    # calculate x,y coordinate of center
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    
    #bboxes = coarse_center_adjustment(bboxes,cX,cY,big_variance)
    bboxes = coarse_center_adjustment(bboxes,cX,cY,res, bound_value)

    
    #print("shape of patch histogram ",ph.shape, np.mean(np.abs(ph-ph)) )



    return bboxes


def size_adjustment(image, rsf,locs,m_idx,bboxes):
    '''
    if type(rsf)!=list:
        rsf = [rsf,rsf]
    '''

    print("got resize suggestion ",rsf)
    box_h = locs[m_idx][2] - locs[m_idx][0]
    box_w = locs[m_idx][3] - locs[m_idx][1]


    
    locs[m_idx][2] = min(image.shape[0], int(locs[m_idx][2] + ( box_h*math.fabs(rsf[0]-1) )/2.0) )
    locs[m_idx][0] = max(0, int(locs[m_idx][0] - ( box_h*math.fabs(rsf[0]-1) )/2.0) )

    locs[m_idx][3] = min(image.shape[1], int(locs[m_idx][3] + ( box_w*math.fabs(rsf[1]-1) )/2.0) )
    locs[m_idx][1] = max(0, int(locs[m_idx][1] - ( box_w*math.fabs(rsf[1]-1) )/2.0) )


    for k in range(3): #trmplate matching box, ssim matching box and the user defined box
        bboxes[k][2] = min(image.shape[0], int(bboxes[k][2] + ( box_h*math.fabs(rsf[0]-1) )/2.0) )
        bboxes[k][0] = max(0, int(bboxes[k][0] - ( box_h*math.fabs(rsf[0]-1) )/2.0) )

        bboxes[k][3] = min(image.shape[1], int(bboxes[k][3] + ( box_w*math.fabs(rsf[1]-1) )/2.0) )
        bboxes[k][1] = max(0,int(bboxes[k][1] - ( box_w*math.fabs(rsf[1]-1) )/2.0) )
    

    
    return locs, bboxes



def fine_adjustment(image,bboxes,small_patch,small_variance,max_ssims_track, patch_striding, nested_region_subsizes, ssim_drop_warning, comparison_functions):
    
    #small_variance = adjust_variance(bboxes,small_variance,image)
    #extract neighborhood patches to the marked region
    patches,locs = extract_neighborhood_patch_proposals(image,small_patch,bboxes[0],small_variance, patch_striding)

    #main part of the algorithm where finally the most similar patch location is calculated
    time1 = time.time()
    metric_scores, rs = sliding_window_metrics(small_patch, patches, nested_region_subsizes, comparison_functions)
    time2 = time.time()
    print("time taken by sliding window metric ",time2-time1)
    nrs = [[1.0,1.0]]
    nrs.extend([e for e in nested_region_subsizes])
    nested_region_subsizes= nrs
    print("changed nested region subsizes ",nested_region_subsizes)
    rsf = nested_region_subsizes[rs]


    #ssims_n, psnrs_n, nrmses_n = np.array(ssims)/np.max(ssims), np.array(psnrs)/np.max(psnrs), np.array(nrmses)/np.max(nrmses)
    #metric = (ssims_n+psnrs_n+nrmses_n)/3.0
    m_idx = np.argmax(metric_scores)
    print("got max metric ",metric_scores[m_idx], "at location ",locs[m_idx])


    #locs, bboxes = size_adjustment(image, rsf,locs,m_idx,bboxes)

    bboxes = fine_center_adjustment(locs[m_idx],bboxes)



    #data quality warning
    max_ssims_track.append(metric_scores[m_idx])
    med_ssim = ssim_drop_warning*np.median(max_ssims_track)
    if metric_scores[m_idx]<med_ssim:
        print("warning ! drastic change has happened, mean ssim so far ", np.mean(max_ssims_track[:-1]))
        print("press esc again to continue")
        #cv2.waitKey(0)
        #reset the max ssim tracking list
        max_ssims_track = []

    return locs[m_idx], bboxes, max_ssims_track


def constant_velocity_update(dist_vector_x,dist_vector_y,location,bboxes, constant_velocity_window):
    #keep track of rate of change of position of tracked patch and smooth it out
    dist_vector_x.append( location[0]-bboxes[0][0] )
    dist_vector_y.append( location[1]-bboxes[0][1] )
    if len(dist_vector_x)>constant_velocity_window:
        adx = np.mean(dist_vector_x[-constant_velocity_window :])
        ady = np.mean(dist_vector_y[-constant_velocity_window :])
    else:
        adx = dist_vector_x[-1]
        ady = dist_vector_y[-1]
    return dist_vector_x,dist_vector_y,adx,ady
