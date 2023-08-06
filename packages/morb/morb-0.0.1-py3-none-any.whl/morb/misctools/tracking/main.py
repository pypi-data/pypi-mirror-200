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
from core_funcs import extract_neighborhood_patch_proposals, nested_regions, sliding_window_metrics, coarse_center_adjustment, fine_center_adjustment, patch_histogram, check_increase_size, coarse_adjustment, size_adjustment, fine_adjustment, constant_velocity_update


import time as t

import os
import sys
import json
import time
import argparse


os.environ['top'] = '../../'
sys.path.append(os.path.join(os.environ['top']))

from datacreators.utils import cv_annotator









parser = argparse.ArgumentParser()
parser.add_argument("-i", "--start_idx", type=int, default=230, help="The index of the image in the tracking folder from where to start tracking")
args = parser.parse_args()






#to do - improve all past tracked boxes and sizes using another final user annotation at the last tracked frame (take weighted averages from start to end)
#to do - extend for tracking multiple regions and taking aggregates to achieve better accuracy/ construct a class


#read image function
def read_with_filtering_convert32(fname, filter_kernel_size):
    #used to degrade vertical resolution
    im = cv2.imread(fname)
    im = im[:,:,0] #got the range image

    im_new = np.zeros((32, im.shape[1]))
    count = 0
    for row in range(0,im.shape[0],4): #take every 4th row
        im_new[count,:] = im[row,:]
        count+=1
    im_new = cv2.resize(im_new,(2048,128))
    #im = median(im, disk(filter_kernel_size))
    return im_new

#read image function
def read_with_filtering(fname, filter_kernel_size):
    #normal function
    im = cv2.imread(fname,0)
    
    #im = cv2.imread(fname)
    #im = im[:,:,0]


    #im = median(im, disk(filter_kernel_size))
    return im





def edit_trackbox(full,all_boxes,trackers):
    print("editing current tracking ")
    print("Initial ", all_boxes)
    ba = cv_annotator.bounding_box_annotator(full,desired_size = (-1,-1), normalize_bbox = False)
    adjust_boxes = [b[2] for b in all_boxes] #index 2 is the user annotated region
    adjusted_boxes, adjustments = ba.adjust(adjust_boxes)

    for tracker_num in range(len(trackers)):
        #l = all_locations[tracker_num]
        b = all_boxes[tracker_num]

        print("check ",adjustments[tracker_num])
        #print("check ",l, b)
        #l = [ l[e] - adjustments[tracker_num][e] for e in range(len(l)) ]
        b[0] = [ int(b[0][e] - adjustments[tracker_num][e]) for e in range(len(b[0])) ]
        b[1] = [ int(b[1][e] - adjustments[tracker_num][e]) for e in range(len(b[0])) ]
        b[2] = [ int(b[2][e] - adjustments[tracker_num][e]) for e in range(len(b[0])) ]
            
        
        #all_locations[tracker_num] = l
        all_boxes[tracker_num] = b
    return all_boxes, adjustments



def visualize(img, boxes, frame_number, draw_patches_also = False):
    full = img
    if len(full.shape)!=3: #not a 3 channel image
        full_viz = np.dstack([full,full,full])
    else:
        full_viz = full

    for i in range(len(boxes)):
        #location = locations[i]
        bboxes = boxes[i]
        track_frame_number = frame_number

        #visualizations
        #convert to rgb so that you can draw rectangle
        


        if draw_patches_also:
            #draw the tracking ssim patch rectangle
            cv2.rectangle(full_viz, (bboxes[0][1], bboxes[0][0]) , (bboxes[0][3], bboxes[0][2]), (0,255,255), 2)
            #draw the tracking template matching patch
            cv2.rectangle(full_viz, (bboxes[1][1], bboxes[1][0]) , (bboxes[1][3], bboxes[1][2]), (255,255,0), 2)
            #put text indicating tracked frame number
            cv2.putText(full_viz, str(track_frame_number), (bboxes[0][1], bboxes[0][0]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)


        #draw the actual user marked bounding box
        cv2.rectangle(full_viz, (bboxes[2][1], bboxes[2][0]) , (bboxes[2][3], bboxes[2][2]), (0,0,255), 1)
        
        #draw the center of the tracking patch
        #center_coordinates = (  int(0.5*(location[1]+location[3] )) , int(0.5*(location[0]+location[2]))   )
        center_coordinates = (  int(0.5*(bboxes[2][1]+bboxes[2][3] )) , int(0.5*(bboxes[2][0]+bboxes[2][2]))   )
        cv2.circle(full_viz, center_coordinates, 2, (0,255,255), -1)
    
    
    return full_viz
    



class tracker(object):
    def __init__(self, start_idx, marked_bounding_box, params):
        self.params = params

        ssim_padding, template_padding, annotation_folder =  params["ssim_padding"], params["template_padding"], params["annotation_folder"]

        bboxes = marked_bounding_box

        im_name = params["tracking_dataset"]+str(start_idx)+'.png'
        #print("got image name ",im_name)
        full = read_with_filtering(im_name, params["filter_kernel_size"])

        self.vmin = 0
        self.vmax = [full.shape[0], full.shape[1]]

        annotate_box = [bboxes[0][0], bboxes[0][1], bboxes[0][2], bboxes[0][3] ]
        ssim_box = [bboxes[0][0]-ssim_padding[0][0] , bboxes[0][1]-ssim_padding[1][0], bboxes[0][2]+ssim_padding[0][1], bboxes[0][3]+ssim_padding[1][1] ]
        template_matching_box = [bboxes[0][0]-template_padding[0][0], bboxes[0][1]-template_padding[1][0], bboxes[0][2]+template_padding[0][1], bboxes[0][3]+template_padding[1][1] ]
        
        bboxes = [ssim_box,template_matching_box,annotate_box]

        ssim_patch = full[bboxes[0][0]:bboxes[0][2], bboxes[0][1]:bboxes[0][3] ]
        

        #make sure the annotation folder is created 
        if not os.path.exists(annotation_folder):
            print("annotation results folder does not exist creating one...")
            os.makedirs(annotation_folder)
            os.makedirs(annotation_folder+"ann/")
            os.makedirs(annotation_folder+"img/")

        template_patch = full[bboxes[1][0]:bboxes[1][2], bboxes[1][1]:bboxes[1][3] ]
        annotate_patch = full[bboxes[2][0]:bboxes[2][2], bboxes[2][1]:bboxes[2][3] ]
        
        dist_vector_x = []
        dist_vector_y = []
        max_ssims = []
        #tracked_boxes = []


        self.state = {"current_image":full,
                     "small_patch": ssim_patch, 
                     "boxes": bboxes,
                     "location":bboxes,
                     "big_patch": template_patch,
                     "annotate_patch":annotate_patch,
                     "dxvector": dist_vector_x,
                     "dyvector": dist_vector_y,
                     "prev_max_ssims": max_ssims,
                     "prev_boxes": []}

        self.past_states = []

        print("Initialized tracker with state ",self.state)

    def reinit_track_regions(self,bboxes):
        ssim_padding, template_padding, annotation_folder =  self.params["ssim_padding"], self.params["template_padding"], self.params["annotation_folder"]

        annotate_box = [bboxes[2][0], bboxes[2][1], bboxes[2][2], bboxes[2][3] ]
        ssim_box = [bboxes[2][0]-ssim_padding[0][0] , bboxes[2][1]-ssim_padding[1][0], bboxes[2][2]+ssim_padding[0][1], bboxes[2][3]+ssim_padding[1][1] ]
        template_matching_box = [bboxes[2][0]-template_padding[0][0], bboxes[2][1]-template_padding[1][0], bboxes[2][2]+template_padding[0][1], bboxes[2][3]+template_padding[1][1] ]
        

        
        bboxes = [ssim_box,template_matching_box,annotate_box]
        full = self.state["current_image"]

        ssim_patch = full[bboxes[0][0]:bboxes[0][2], bboxes[0][1]:bboxes[0][3] ]

        template_patch = full[bboxes[1][0]:bboxes[1][2], bboxes[1][1]:bboxes[1][3] ]
        annotate_patch = full[bboxes[2][0]:bboxes[2][2], bboxes[2][1]:bboxes[2][3] ]

        self.state["small_patch"] =  ssim_patch
        self.state["boxes"] =  bboxes
        self.state["location"] = bboxes
        self.state["big_patch"] =  template_patch
        self.state["annotate_patch"] = annotate_patch

        dist_vector_x = self.state["dxvector"]
        dist_vector_y = self.state["dyvector"]
        max_ssims = self.state["prev_max_ssims"]

        dist_vector_x.pop(-1)
        dist_vector_y.pop(-1)
        max_ssims.pop(-1)

        self.state["dxvector"] =  dist_vector_x
        self.state["dyvector"] =  dist_vector_y
        self.state["prev_max_ssims"] =  max_ssims


    
    def bound_value(self, v, axis):
        #print("bound value input ",v)
        if v< self.vmin:
            #print("bounding !")
            return self.vmin
        elif v> self.vmax[axis]:
            #print("bounding ! ")
            return self.vmax[axis]
        else:
            return v

    def rollback(self):
        cimg = self.state["current_image"]
        if len(self.past_states)>0:
            self.state = self.past_states.pop(-1)
            self.state["current_image"] = cimg
        else:
            print("cannot roll back anymore")

    def track(self, idx):

        state = self.state
        params = self.params

        #unpack state variables
        ssim_patch = self.state["small_patch"]
        template_patch = self.state["big_patch"]
        annotate_patch = self.state["annotate_patch"]
        bboxes = self.state["boxes"]
        dist_vector_x = self.state["dxvector"]
        dist_vector_y = self.state["dyvector"]
        max_ssims = self.state["prev_max_ssims"]
        #tracked_boxes = self.state["prev_boxes"]

        self.past_states.append(copy.deepcopy(self.state))



        #im_name = params["tracking_dataset"]+str(idx)+'.png'
        #full = read_with_filtering(im_name, params["filter_kernel_size"])

        full = self.state["current_image"]


        time1 = time.time()
        #coarse adjustment uses just template matching
        bboxes = coarse_adjustment(full,bboxes,template_patch,params["big_variance"], self.bound_value)
        time2 = time.time()
        print("coarse adjustment took ",time2-time1) #0.001


        time1 = time.time()
        #fine adjustment uses a list of comparison metrics that the user can pass
        location, bboxes, max_ssims = fine_adjustment(full,bboxes,ssim_patch,params["small_variance"], max_ssims, params["patch_striding"], params["nested_region_subsizes"], params["ssim_drop_warning"], params["comparison_functions"])
        time2 = time.time()
        print("fine adjustment took ",time2-time1) #0.045
        
        

        #can use the assumption that camera is moving at constant velocity wrt the object so centers should shift uniformly and not jerky
        dist_vector_x, dist_vector_y,adx,ady =  constant_velocity_update(dist_vector_x,dist_vector_y,location,bboxes, params["constant_velocity_window"])

        


        #update box locations, ssim,template and actual
        bboxes[0] = [int(adx+bboxes[0][0])  ,  int(ady+bboxes[0][1]),  int(adx+bboxes[0][2])  ,  int(ady+bboxes[0][3])    ]
        bboxes[1] = [int(adx+bboxes[1][0])  ,  int(ady+bboxes[1][1]),  int(adx+bboxes[1][2])  ,  int(ady+bboxes[1][3])    ]
        bboxes[2] = [int(adx+bboxes[2][0])  ,  int(ady+bboxes[2][1]),  int(adx+bboxes[2][2])  ,  int(ady+bboxes[2][3])    ]
        
        




        #run a final check to see if sizes of boxes to track have changed because object moved closer/farther
        if params["check_increase_size"]:
            bboxes = check_increase_size(full,bboxes,annotate_patch)



        #update regions to track for next iteratuve tracking - ssim and template regions
        
        #ssim_patch = full[location[0]:location[2], location[1]:location[3] ]
        ssim_patch = full[bboxes[0][0]:bboxes[0][2], bboxes[0][1]:bboxes[0][3] ]
        template_patch = full[bboxes[1][0]:bboxes[1][2], bboxes[1][1]:bboxes[1][3] ]
        annotate_patch = full[bboxes[2][0]:bboxes[2][2], bboxes[2][1]:bboxes[2][3] ]
        


        track_frame_number = idx#-mark_idx

        #tracked_boxes = self.past_states[-1]["boxes"]
        
        im_name = params["tracking_dataset"]+str(idx)+'.png'
        full = read_with_filtering(im_name, params["filter_kernel_size"])
        #pack state variables
        self.state = {"current_image":full,
                     "small_patch": ssim_patch, 
                     "boxes": bboxes,
                     "location":location,
                     "big_patch": template_patch,
                     "annotate_patch": annotate_patch,
                     "dxvector": dist_vector_x,
                     "dyvector": dist_vector_y,
                     "prev_max_ssims": max_ssims}












if __name__ == '__main__':
    
    #tracking dataset should be a folder that contains the sequence of images
    #all the file names in the tracking dataset should end with _<index number>.png

    division = 1
    mark_idx = args.start_idx  #350, 316
    print("supplied starting index ",mark_idx)
    num_trackings = 35 
    #doesnt perform well if too num_tracking is too big, naturally because of the nature of motion which can cause 
    #drastic changes in size of object to track/introduce sudden new objects from hidden field of views which introduces drift gradually over time

    #Note- On top of params, the quility of annotation may also be affected by the initial marked box by user
    #if tracking in struggling, make sure to select wider and taller boxes that also include slight surroundings around the feature

    #Note ! - check_increase_size can increase size of track box by using some checks but doesnt always work well, so can pass false also in params
    #Note ! - in comparison functions can only pass [psnr] it will slightly reduce accuracy but will increase speed around 2 times -> 4 boxes at 50ms compared to 4 boxes at 100ms

    comp_funcs = [ssim,psnr,nrmse]
    #comp_funcs = [psnr]
    
    params_big = {"tracking_dataset": '/datasets/lidar_post_detection/extracted_lidar_data/'+str(division)+'_',
              "annotation_folder": 'tracking_annotations/',
              "small_variance": [5,5],
              "big_variance": [5,30],
              "ssim_padding": [[0,7],[10,10]],
              "template_padding": [[-10,20],[25,25]],
              "filter_kernel_size": 1,
              "patch_striding": (1,1),
              "nested_region_subsizes": [],
              "constant_velocity_window": 2,
              "ssim_drop_warning": 0.75,
              "check_increase_size":False,
              "comparison_functions": comp_funcs}
    

    
    #for small posts that are far away and move slowly 246
    params_small = {"tracking_dataset": '/datasets/lidar_post_detection/extracted_lidar_data/'+str(division)+'_',
              "annotation_folder": 'tracking_annotations/',
              "small_variance": [5,5],
              "big_variance": [2,10],
              "ssim_padding": [[5,7],[10,10]],
              "template_padding": [[10,20],[25,25]],
              "filter_kernel_size": 1,
              "patch_striding": (1,1),
              "nested_region_subsizes": [],
              "constant_velocity_window": 2,
              "ssim_drop_warning": 0.75,
              "check_increase_size":False,
              "comparison_functions": comp_funcs}

    params_medium = {"tracking_dataset": '/datasets/lidar_post_detection/extracted_lidar_data/'+str(division)+'_',
              "annotation_folder": 'tracking_annotations/',
              "small_variance": [5,5],
              "big_variance": [3,20],
              "ssim_padding": [[2,7],[10,10]],
              "template_padding": [[5,20],[25,25]],
              "filter_kernel_size": 1,
              "patch_striding": (1,1),
              "nested_region_subsizes": [],
              "constant_velocity_window": 2,
              "ssim_drop_warning": 0.75,
              "check_increase_size":False,
              "comparison_functions": comp_funcs}
    






    #show the starting image
    im_name = params_big["tracking_dataset"]+str(mark_idx)+'.png'
    print("got image name ",im_name)
    full = read_with_filtering(im_name, params_big["filter_kernel_size"])
    cv2.imshow("full image ",full)
    cv2.waitKey(0)


    #annotate all the boxes in the starting image
    ba = cv_annotator.bounding_box_annotator(full,desired_size = (-1,-1), normalize_bbox = False)
    marked_boxes = ba.run()
    print("Final all bounding boxes ...")
    print(marked_boxes)




    #based on user annotations get the areas of the boxes and chose parameters based on selected area sizes
    areas = []
    for m in marked_boxes:
        area = (m[0]-m[2])*(m[1]-m[3])
        print("marked box area ",area)
        areas.append(area)


    params = []
    for a in range(len(areas)):
        if areas[a]>3000:
            params.append(params_big)
        elif areas[a]<400:
            params.append(params_small)
        elif areas[a]>=400 and areas[a]<=3000:
            params.append(params_medium)







    #initialize one tracker class for each box
    trackers = [tracker(mark_idx, [marked_boxes[m]], params[m]) for m in range(len(marked_boxes))]
    

    #do the tracking
    i = mark_idx
    while i<mark_idx+num_trackings:
        print("image index ",i)
        full =  trackers[0].state["current_image"] 
        
        #all_locations = []
        time1 = time.time()
        all_boxes = []
        for t in trackers:
            
            t.track(i)
            
            #all_locations.append(t.state["location"])
            
            all_boxes.append(t.state["boxes"])
            

        time2 = time.time()
        print("time taken for tracking ",time2-time1)
        #visualize each step of the tracking
        full = visualize( full, all_boxes, i)
        cv2.imshow("ssim located patch ",full)
        k = cv2.waitKey(0)
        

        
        #option for user to edit the tracking box in between tracking
        #just select the edge of the box and drag it in adjusting image window
        if k==101 : #ord('e')

            all_boxes,_ = edit_trackbox(full,all_boxes,trackers)

            for n in range(len(trackers)):
                trackers[n].reinit_track_regions(copy.deepcopy(all_boxes[n]))

            #edited = visualize( full, all_locations, all_boxes, i)
            edited = visualize( full, all_boxes, i)
            cv2.imshow("ssim located patch ",edited)
            print("adjusted  ", all_boxes)
            cv2.waitKey(0)
        


        #stop all tracking
        if k ==115 : #ord('s')
            print("ending current tracking ")
            num_trackings = i - mark_idx #log the trackings till the prev frame
            break

        i+=1

    



    #save the tracked bounding boxes
    inp = input("save the tracked annotations ? (y/n) ")
    if inp=='y':

        accum_adjustment = [  np.array([0,0,0,0])  for _ in trackers]
        adjustment_step = [  np.array([0,0,0,0])  for _ in trackers]

        inp1 = input("Do you want to back adjust from the final frame annotation ? (y/n) ")
        
        if inp1=='y':
            all_boxes, adjustments = edit_trackbox(full,all_boxes,trackers)
            edited = visualize( full, all_boxes, 1) #last parameter does not matter
            print("got final adjustments ",adjustments)

            adjustment_step = [ np.array(a)/(num_trackings-2)  for a in adjustments]
            




        count=0
        for i in range(mark_idx+1, mark_idx+num_trackings-1):
            # i-mark_idx+1 is the tracked box index for the image number i-mark_idx and actual image number i
            
            folder = params[0]["annotation_folder"]
            imfile = params[0]["tracking_dataset"]+str(i-1)+'.png'



            full = read_with_filtering(imfile, params_big["filter_kernel_size"])
            

            accum_adjustment = [  accum_adjustment[e] + adjustment_step[e]   for e in range(len(adjustment_step)) ] 
            
            #full = visualize( full, all_boxes_time[i-mark_idx], i)
            #full = visualize( full, [t.past_states[i-mark_idx+1]["boxes"] for t in trackers], i)
            
            all_boxes_backadjust = []

            for num in range(len(trackers)):
                boxes = trackers[num].past_states[i-mark_idx+1]["boxes"]
                boxes_back_adjusted = [ list(   np.asarray( np.array( boxes[e] ) - accum_adjustment[num], dtype=int)   ) for e in range(len(boxes))  ]
                
                all_boxes_backadjust.append(boxes_back_adjusted)
            
            
            full = visualize( full, all_boxes_backadjust, i)
            cv2.imshow("final tracked backadjusted annotation ",full)
            k = cv2.waitKey(0)


            
            for n in range(len(trackers)):
                #save image and annotations in supervisely style
                #print("check ", trackers[n].past_states[i-mark_idx+1]["boxes"][2])
                #print("check ",all_boxes_backadjust[n][2])
                save_box = [int(e) for e in all_boxes_backadjust[n][2]]

                #cv_annotator.save_annotations(folder, imfile, i, trackers[n].past_states[i-mark_idx+1]["boxes"][2], read_with_filtering_convert32) #index 2 tracks the real annotation
                cv_annotator.save_annotations(folder, imfile, i, save_box, read_with_filtering_convert32) #index 2 tracks the real annotation
            count+=1

        print("number of images annotated and saved ",count)


