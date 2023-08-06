
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

from dataloaders import cihp
from models.pytorch import unet




if __name__ == '__main__':
    model = unet.Network(1)
    dataloader = cihp.dataloader()

    T = train_seg.trainloop(model,dataloader, segment.seg_loss)
    T.load_prev_weights()
    T.fit(num_batches = 100000)
