
import tensorflow as tf
from tensorflow.keras.layers import *
import numpy as np
import math
import cv2
import glob
import os
from PIL import Image
import sys


import os
os.environ['top'] = '../../'
sys.path.append(os.path.join(os.environ['top']))
from custom_losses.tensorflow import feature_detect




#================================================================
#============Conversion functions================================

def combined_model():
    #initially all the lidar data comes in as a 1d data, but it comprises of 16 rings each having 1800 points
    #so first normalize it and then reshape it as a 2d image
    #then resize the 2d image for ML input
   
    #preprocessing layers baked into model
    #so that we can work directly on raw data from the drivers

    lidar_hor = 1800
    lidar_ver = 16
    avg_max_value = 50 #used 50 for OS0 and OS1 128 channel
    col_idx_min = 100
    col_idx_max = 750

    model_img_height = 64
    model_img_width = 1024

    trained_model_path = 'kpmodel'


    inputs = Input(shape=(lidar_ver*lidar_hor,))
    x = tf.keras.layers.Reshape((lidar_ver, lidar_hor, 1), input_shape=(lidar_ver*lidar_hor,))(inputs)
    x = x/avg_max_value
    x = tf.image.resize(x, [model_img_height, model_img_width])
    #current cropping technique - https://www.tensorflow.org/api_docs/python/tf/keras/layers/Cropping2D
    x = tf.keras.layers.Cropping2D(cropping=((0, 0), (col_idx_min, model_img_width-col_idx_max)))(x)
    
    
    model = tf.keras.models.load_model(trained_model_path, custom_objects={'class_loss': feature_detect.class_loss, 'reg_loss':feature_detect.reg_loss})
    output = model(x)
    #now we should have normalized and reshaped lidar image
    #can try multi output models if preprocessed is also needed
    #combined = tf.keras.Model(inputs = inputs, outputs = [preprocessed,output])

    #need to process the final output to scale it to the machine operator controls


    combined = tf.keras.Model(inputs = inputs, outputs = output)
    #print(combined.summary())
    #sys.exit(0)
    return combined



def convert_combined_model():
    comb = combined_model()
    #comb = simple_model()

    converter = tf.lite.TFLiteConverter.from_keras_model(comb)
    tflite_model = converter.convert()
    # Save the model.
    with open('kpmodel.tflite', 'wb') as f:
      f.write(tflite_model)






        

if __name__ == '__main__':

    #test successful conversions
    print("converting the combined model ")
    convert_combined_model()
    
    
