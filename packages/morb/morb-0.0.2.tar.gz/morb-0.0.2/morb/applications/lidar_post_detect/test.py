import tensorflow as tf
from tensorflow.keras.layers import *
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import backend as K
from tensorflow.keras.models import Sequential,Model
from tensorflow.keras.optimizers import Adam
import sys




import numpy as np
import cv2

import copy
from ouster import client, pcap

from datetime import datetime as dt
import time

import os
os.environ['top'] = '../../'
sys.path.append(os.path.join(os.environ['top']))
from custom_losses.tensorflow import feature_detect
from misctools.edge_detect import classic_edge_detect

from dataloaders import imgcsvloader

from visualizers import extract_lidar_data
from dataloaders.utils import read_supervisely
from models.tensorflow.object_detection import sliding_window_conv
from models.tensorflow.utils import signal_processing_layers

import params



smoothing = signal_processing_layers.Smoothing(input_shape = (64,650,1))



probe_model_input_output = imgcsvloader.probe_model_input_output

n_kp = params.num_pred_regions

desired_size = (1024,64)

#dataset_name = '/datasets/lidar_post_detection/raw_lidar_data/channel32/1/'

#dataset_name = '/datasets/lidar_post_detection/raw_lidar_data/'+'channel128_narrow_angle/'+str(1)+'/'
dataset_name = '/datasets/lidar_post_detection/raw_lidar_data/'+'channel128_wide_angle/'+str(1)+'/'

pcap_path = dataset_name+'lidar/os.pcap'
metadata_path = dataset_name+'lidar/os.json'

count_frames = True

start_from = 180



def extract_from_raw_lidar_and_predict(m):
    count = 0
    with open(metadata_path, 'r') as f:
        metadata = client.SensorInfo(f.read())

    source = pcap.Pcap(pcap_path, metadata)

    scans = iter(client.Scans(source))
    count = 0
    mvap = {"moving_window_size":2, "variance_capture": [5,5] }

    for idx, scan in enumerate(scans):
        count+=1
        if count_frames:
            print("Frame number ",count)

        loaded_image = extract_lidar_data.extract_image(source, scan)
        model_input_image = read_supervisely.convert_from_original_scale_image(loaded_image, degrade_vres = True)



        #visualize the signal processing smoothing layer if you want
        '''
        smoothed_input = smoothing.median_layer(model_specific_convert_for_test(model_input_image))
        inp = np.array(smoothed_input)
        inp = cv2.resize(inp,(650,256))
        cv2.imshow("smoothed input ",inp)
        cv2.waitKey(10)
        '''





        if count<start_from:
            print("not inferencing on this frame")
            continue






        #x = model_specific_convert_for_test(ring_norm_img)
        x = model_specific_convert_for_test(model_input_image)

        
        yc, yr = m.predict(x)
        y = tf.keras.layers.concatenate([yc,yr], axis=3)

        
        
        #mvap = probe_model_input_output(x,y[0], "model output", confidence_thresh = 0.5, resize_height = 128, moving_average_pred = mvap)
        probe_model_input_output(x,y[0], "model output", confidence_thresh = 0.5, resize_height = 128)
        



#0, 5000
#550,1100

#"/datasets/danfoss/lidar_person/supervisely_annotated/img/"
# name_range = [600,1100]

def predict_on_image_folder(m, imfolder = params.test_images_folder, name_range = [150,450]): #305
    #expects imfolder to contain sequentially named images without integer gaps eg- 1.png,2.png...
    prefix = "frame"
    prefix = "1_"

    for i in range(name_range[0], name_range[1]):
        #loaded_image = extract_lidar_data.extract_image(source, scan)
        file = imfolder+prefix+str(i)+'.png'
        if(os.path.exists(file) ==False):
            continue
        
        if params.test_image_preprocessing=="plain_read":
            loaded_image = cv2.imread(file)
        
        if params.test_image_preprocessing=="edge_detect":
            #for transfer based object detection (there is some potential but lots of false positives for now need bigger model probably)
            loaded_image = classic_edge_detect.obtain_contours(imfilename = file, resize_s = (params.model_image_input_width, params.model_input_image_height), outputfile = "")
            
            
            # loaded_image = loaded_image[:,:,0]
            # loaded_image = cv2.resize(loaded_image,(512,64))
            # loaded_image = canny(loaded_image)
        
        

        print("frame number ",i)

        model_input_image = read_supervisely.convert_from_original_scale_image(loaded_image, degrade_vres = False, channel_selection=-1)
        
        x = model_specific_convert_for_test(model_input_image, normalize = 255.0)

        
        yc, yr = m.predict(x)
        y = tf.keras.layers.concatenate([yc,yr], axis=3)

        #if edge detect mode used then again reload the proper unprocessed image
        if params.test_image_preprocessing=="edge_detect":
            probe_model_input_output(x,y[0], "processed model output", confidence_thresh = params.output_conf_thresh, moving_average_pred = params.mvap)
            loaded_image = cv2.imread(file)
            model_input_image = read_supervisely.convert_from_original_scale_image(loaded_image, degrade_vres = False, channel_selection=-1)
            x = model_specific_convert_for_test(model_input_image, normalize = 255.0)

        
        #mvap = probe_model_input_output(x,y[0], "model output", confidence_thresh = 0.5, resize_height = 128, moving_average_pred = mvap)
        probe_model_input_output(x,y[0], "model output", confidence_thresh = params.output_conf_thresh)





def model_specific_convert_to_tensor(inputs,outputs):
    x = tf.convert_to_tensor(np.array(inputs), dtype=tf.float32)
    y = tf.convert_to_tensor(np.array(outputs), dtype=tf.float32)
    
    return x, y

def model_specific_convert_for_test(inputs, normalize = 1.0):
    inputs = np.array(inputs/normalize, dtype = np.float32)
    #inputs = inputs.reshape((1,64,650))
    inputs = inputs.reshape((1,64,512))

    x = tf.convert_to_tensor(np.array(inputs), dtype=tf.float32)
    return x




if __name__ == '__main__':
    
    
    trained_model_path = 'kpmodel'



    model = tf.keras.models.load_model(trained_model_path, custom_objects={'class_loss': feature_detect.class_loss, 'reg_loss':feature_detect.reg_loss})

    #model = tf.keras.models.load_model(trained_model_path)
    #model = load_model('my_model.h5', custom_objects={'my_custom_func': feature_detect.loss})
    print(model.summary())
    print("successfully loaded model weights")
    
    #directly extract from pcap files, process and predict through loaded model
    #extract_from_raw_lidar_and_predict(model)

    #predict on sequentially named images in an images folder
    predict_on_image_folder(model)
    
    


    



