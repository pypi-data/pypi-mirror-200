import tensorflow as tf
from tensorflow.keras.layers import *
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import backend as K
from tensorflow.keras.models import Sequential,Model
from tensorflow.keras.optimizers import Adam
import os
import sys

os.environ['top'] = '../../'
sys.path.append(os.path.join(os.environ['top']))

from trainers.tensorflow.object_detection import sliding_window_train

from custom_losses.tensorflow import feature_detect

from dataloaders import imgcsvloader
from models.tensorflow.object_detection import sliding_window_conv, patch_net

import params


if __name__ == '__main__':
    model = sliding_window_conv.Network(height= params.model_input_image_height, width=params.model_image_input_width, use_median_layer = params.use_median_prelayer)
    #model = patch_net.Network(use_median_layer = params.use_median_prelayer)

    dataloader = imgcsvloader.dataloader()

    #customizations
    if params.use_median_prelayer: #tfa.image.median function doesnt work across batches
        dataloader.batch_size = 1 #if using median layer in the network, sorry you must use batch size=1 otherwise would not be able to load model in test

    else:
        dataloader.batch_size = 32
    
    object_detection_loss =  {
                                model.classif_layer_name : feature_detect.class_loss,
                                model.reg_layer_name : feature_detect.reg_loss,
                            }

    T = sliding_window_train.trainloop(model,dataloader, object_detection_loss)
    #T.load_prev_weights()
    T.fit(batches = 100000)
