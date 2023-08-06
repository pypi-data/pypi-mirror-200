import cv2
import numpy as np
import open3d as o3d
import math

import sys
import os

os.environ['top'] = '../../'
sys.path.append(os.path.join(os.environ['top']))
from visualizers import pointcloud


vidcap = cv2.VideoCapture('iphone_depth_sample3.MP4')
success,image = vidcap.read()




def read_extract_frames_from_movie():
  success = True
  count = 0
  stopat = 200
  if not os.path.exists("test"):
    os.mkdir("test")
  
  while success:
    success,image = vidcap.read()
    #cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
    cv2.imwrite("test/"+str(count)+".png", image)     # save frame as JPEG file
    if cv2.waitKey(10) == 27:                     # exit if Escape is hit
      break
    if count==stopat:
      break
    count += 1





def load_verify_extracted(indices):
  #verify is checkerboard properly visible in calib indices images
  rgbs = []
  depths = []

  for c in indices:
    img = cv2.imread("test/"+str(c)+".png")

    desired_size = (256,256)

    img = cv2.resize(img,(desired_size[0]*2, desired_size[1]))
    print(img.shape) #(1504, 1128, 3)

    width = img.shape[1]
    height = img.shape[0]

    '''
    cv2.imshow("extracted ",img)
    cv2.waitKey(0)

    depth = img[:,width//2:]
    depth = cv2.cvtColor(depth, cv2.COLOR_BGR2GRAY)
    cv2.imshow("depth ",depth)
    cv2.waitKey(0)
    '''
    depth = img[:,width//2:]
    depth = cv2.cvtColor(depth, cv2.COLOR_BGR2GRAY)
    
    depths.append(depth)
    rgb = img[:,:width//2]
    rgbs.append(rgb)

    '''
    cv2.imshow("depth ",depth)
    cv2.imshow("rgb ",rgb)
    cv2.waitKey(0)
    '''
    

  return rgbs,depths


#read_extract_frames_from_movie()
indices = [190]

rgbs,depths = load_verify_extracted(indices)

iphone_front_camera_params = {
                        "fx": 2*118.62,
                        "fy": 2*99.79,
                        "centerX": 165.91,
                        "centerY": 175.91,
                        "scalingFactor": 1
                    }

pointcloud.show_pcd_from_rgbd(rgbs[0], depths[0], iphone_front_camera_params, transformations = {"rx":180,"ry":0,"rz":0}, save_loc = "2.pcd")


