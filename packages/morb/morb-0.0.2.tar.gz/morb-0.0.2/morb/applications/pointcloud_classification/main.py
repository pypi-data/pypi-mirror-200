
import torch


import os
import sys

os.environ['top'] = '../../'
sys.path.append(os.path.join(os.environ['top']))

from trainers.pytorch import train_pointcloud
from custom_losses.pytorch import pointnetloss
from dataloaders import modelnet
from models.pytorch import pointnet




if __name__ == '__main__':
    model = pointnet.PointNet_classif(classes = 10)
    dataloader = modelnet.dataloader()
    dataloader.batch_size = 4

    

    optimizer = torch.optim.SGD(model.parameters(), lr=0.00025, momentum=0.9, weight_decay=0.0001)


    T = train_pointcloud.trainloop(model,dataloader, pointnetloss.loss, optimizer = optimizer)
    
    
    #T.weight_save_path = "ade20kweights.pth"
    #T.load_prev_weights()

    T.fit(num_batches = 100000)
