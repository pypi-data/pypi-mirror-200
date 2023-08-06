import os
import sys
#import bottleneck as bn
from ouster import client, pcap
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib.colors import hsv_to_rgb

import cv2
import copy


#this is a nice size for convolution filters as its not TOO big as well as have size in power of 2
desired_size = (2048,128)
#width_crop = [100,750]
width_crop = [0,2048]

data_division = 1
dataroot = "/datasets/lidar_post_detection/raw_lidar_data/"
#dataset_name = 'channel32/'+str(data_division)+'/'
#dataset_name = 'channel128_narrow_angle/'+str(data_division)+'/'
dataset_name = 'channel128_wide_angle/'+str(data_division)+'/'


dataroot = "/datasets/danfoss/lidar_person/raw/"
dataset_name = str(data_division)+'/'


pcap_path = dataroot+dataset_name+'lidar/os.pcap'
metadata_path = dataroot+dataset_name+'lidar/os.json'


normalize_value = [30000,100,100,50] #for 32 channel using 15, for 128 channel using 50
lidar_channel = 'signal' #use near_ir for detecting the circle
count_frames = True
pause_each = False


#save_loc = dataset_name+'extracted/lidar_'+lidar_channel+'/'
save_loc = "/datasets/lidar_post_detection/"+'extracted_lidar_data/'
save_every = 1

start_save = 0
end_save = 3000



if os.path.exists(save_loc):
    import shutil
    inp = input("save path location already exists, delete and create fresh ? (y/n) ")
    if inp=='y':
        print("deleting save loc and creating fresh ")
        shutil.rmtree(save_loc)
        print("deleted")
        os.makedirs(save_loc)

#================================
#all different types of normalizations

def get_max_ignore_outliers(arr):
    arr_flat = arr.flatten()
    top_n_idx = int(len(arr_flat)*0.0005)
    #return np.median(-bn.partition(-arr_flat, top_n_idx)[:top_n_idx])
    return np.median(-np.partition(-arr_flat, top_n_idx)[:top_n_idx])

def ring_norm(range_rs):
    #print(np.max(range_rs))
    #return range_rs/90000.0
    
    #my special normalization produces nice contrast on actual lidar data
    range_rs = np.nan_to_num(range_rs)
    range_rs[range_rs==0]=1 #the nan values that got converted to 0, assume they are very close points

    col_max = range_rs.max(axis=1)
    range_rs = range_rs/col_max[:,np.newaxis]

    ring_max = range_rs.max(axis=0)
    ring_norm = range_rs/ring_max[np.newaxis,:]
    #full_norm = (ring_norm-np.mean(ring_norm))/(np.max(ring_norm)-np.min(ring_norm))
    full_norm = (ring_norm)/np.max(ring_norm)
    return full_norm
    

def inverse_norm(range_rs):
    #inverse normalization (closer is whiter)
    #used this in gazebo simulations
    inv_thresh = 500.0
    range_rs = np.nan_to_num(range_rs)
    range_rs[range_rs==0]=(1/inv_thresh)
    inv_norm = inv_thresh/range_rs
    inv_norm[inv_norm>1] = 1.0
    full_norm = inv_norm 
    return full_norm

def easy_norm(range_rs, chan_num):
    print("max value ",np.max(range_rs))
    if normalize_value=='max':
        div = np.max(range_rs)
    else:
        div = normalize_value[chan_num] #15000 (range), 500 (ambient)
    result = range_rs/div
    result[result>div]=div
    return result

#ouster_normalize = easy_norm

def ouster_normalize(data: np.ndarray, channel_num: int = 0, percentile: float = 0.05):
    """Normalize and clamp data for better color mapping.
    This is a utility function used ONLY for the purpose of 2D image
    visualization. The resulting values are not fully reversible because the
    final clipping step discards values outside of [0, 1].
    Args:
        data: array of data to be transformed for visualization
        percentile: values in the bottom/top percentile are clambed to 0 and 1
    Returns:
        An array of doubles with the same shape as ``image`` with values
        normalized to the range [0, 1].
    """
    min_val = np.percentile(data, 100 * percentile)
    max_val = np.percentile(data, 100 * (1 - percentile))
    # to protect from division by zero
    spread = max(max_val - min_val, 1)
    field_res = (data.astype(np.float64) - min_val) / spread
    return field_res.clip(0, 1.0)


#==============================================


def load_channel(lidar_channel, scan):
    if lidar_channel=='range':
        range_field = scan.field(client.ChanField.RANGE)
    if lidar_channel=='near_ir':
        range_field = scan.field(client.ChanField.NEAR_IR)
    if lidar_channel=='signal':
        range_field = scan.field(client.ChanField.SIGNAL)
    if lidar_channel=='reflect':
        range_field = scan.field(client.ChanField.REFLECTIVITY)
    return range_field



def extract_image(source, scan):
    range_field = load_channel('range', scan)
    near_field = load_channel('near_ir', scan)
    signal_field = load_channel('signal', scan)
    reflect_field = load_channel('reflect', scan)

    #destagger each channel
    range_img = client.destagger(source.metadata, range_field).astype('float')
    near_img = client.destagger(source.metadata, near_field).astype('float')
    signal_img = client.destagger(source.metadata, signal_field).astype('float')
    reflect_img = client.destagger(source.metadata, reflect_field).astype('float')

    #normalize each individual channel
    range_img = ouster_normalize(range_img,0)
    near_img = ouster_normalize(near_img,1)
    #near_img = inverse_norm(near_img)
    #near_img = ring_norm(near_img)
    signal_img = ouster_normalize(signal_img,2)
    reflect_img = ouster_normalize(reflect_img,3)


    input_img = np.dstack([range_img,signal_img,reflect_img])
    #input_img = np.dstack([range_img,range_img,range_img])
    #input_img = np.dstack([range_img,reflect_img,near_img])
    input_img = cv2.resize(input_img, desired_size)
    input_img = input_img[:,width_crop[0]:width_crop[1]]

    return input_img



if __name__ == '__main__':
    count = 0
    with open(metadata_path, 'r') as f:
        metadata = client.SensorInfo(f.read())

    source = pcap.Pcap(pcap_path, metadata)

    scans = iter(client.Scans(source))
    count = 0
    for idx, scan in enumerate(scans):
        count+=1
        if count_frames:
            print("Frame number ",count)



        if count>start_save: #and count<end_save:
	        input_img = extract_image(source, scan)





	        cv2.imshow(' normalized image ',input_img)
	        #cv2.imshow('ring normalization cropped ',ring_norm_cropped)
	        #print("saving to location ", save_loc+str(count)+'.png')
	        if count%save_every==0:
	            #cv2.imwrite(save_loc+dataset_name[:-1]+'_'+str(count)+'.png',range_img*255.0)
	            cv2.imwrite(save_loc+str(data_division)+'_'+str(count)+'.png',input_img*255.0)
	        #cv2.imwrite(img_extraction_folder+str(count)+'.png',ring_norm_img*255.0)
	        if pause_each:
	            cv2.waitKey(0)
	        else:
	            cv2.waitKey(1)
        
        elif count>end_save:
        	print("mentioned not to save after this Frame ")
        	break
    


