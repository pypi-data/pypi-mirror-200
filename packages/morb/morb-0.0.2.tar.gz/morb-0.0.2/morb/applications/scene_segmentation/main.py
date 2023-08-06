
import torch
import cv2
from torch.utils import data
from torch import nn as nn
from torchvision import models

import torch.nn.functional as F
from glob import glob
import numpy as np
import random

import time 
import copy

import os
import sys

os.environ['top'] = '../../'
sys.path.append(os.path.join(os.environ['top']))

from trainers.pytorch import train_seg

from custom_losses.pytorch import segment

from dataloaders import ade20k
from models.pytorch import deeplabv3




if __name__ == '__main__':
    model = deeplabv3.Network(pretrained = True, num_classes = 151, num_groups = None, weight_std = False, beta = False)
    dataloader = ade20k.dataloader(n_classes = 151)
    dataloader.batch_size = 16

    

    optimizer = torch.optim.SGD(model.parameters(), lr=0.00025, momentum=0.9, weight_decay=0.0001)



    T = train_seg.trainloop(model,dataloader, segment.crossentropy, optimizer = optimizer)
    
    
    T.weight_save_path = "ade20kweights.pth"

    T.load_prev_weights()
    T.fit(num_batches = 100000)
