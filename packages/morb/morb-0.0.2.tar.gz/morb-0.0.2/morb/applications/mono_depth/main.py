
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

from custom_losses.pytorch import depth

from dataloaders import nyuv2
from models.pytorch import feature_pyramid




if __name__ == '__main__':
    model = feature_pyramid.Network()
    dataloader = nyuv2.dataloader("/datasets/nyuv2/")

    #customizations
    dataloader.batch_size = 16
    

    T = train_seg.trainloop(model,dataloader, depth.loss)
    #T.load_prev_weights()
    T.fit()
