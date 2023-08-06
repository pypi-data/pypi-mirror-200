
import torch


import os
import sys

os.environ['top'] = '../../'
sys.path.append(os.path.join(os.environ['top']))

from trainers.pytorch import train_pointcloud
from custom_losses.pytorch import pointnetloss

#nuscenes
from dataloaders.lidar_datasets import loader

#shapenet
#from dataloaders import shapenet as loader


from models.pytorch import pointnet




if __name__ == '__main__':
    model = pointnet.PointNet_seg(classes = 5)

    dataloader = loader.dataloader()

    dataloader.batch_size = 1 #always use 1 for now


    viz_pred_func = loader.probe_segmentation_input_output

    T = train_pointcloud.trainloop(model,dataloader, pointnetloss.loss_seg, viz_pred_func = viz_pred_func)
    
    #print("loading previous weights ")
    #T.load_prev_weights()

    T.fit(num_batches = 100000)
