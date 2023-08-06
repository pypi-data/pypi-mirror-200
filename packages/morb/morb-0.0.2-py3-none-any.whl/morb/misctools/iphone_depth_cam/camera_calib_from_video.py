import cv2
import numpy as np
import open3d as o3d
import math

import sys
import os

os.environ['top'] = '../'
sys.path.append(os.path.join(os.environ['top']))
from visualizers import pointcloud


vidcap = cv2.VideoCapture('checkerboard.MP4')
success,image = vidcap.read()


exponential_returns = False

read_first = True


def read_extract_frames_from_movie():
  success = True
  count = 0
  stopat = 200
  if not os.path.exists("extracted"):
    os.mkdir("extracted")
  
  while success:
    success,image = vidcap.read()
    #cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
    cv2.imwrite("extracted/"+str(count)+".png", image)     # save frame as JPEG file
    if cv2.waitKey(10) == 27:                     # exit if Escape is hit
      break
    if count==stopat:
      break
    count += 1





def load_verify_checkerboard_visibility(calib_indices):
  #verify is checkerboard properly visible in calib indices images
  rgbs = []

  for c in calib_indices:
    img = cv2.imread("extracted/"+str(c)+".png")

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

    rgb = img[:,:width//2]
    cv2.imshow("rgb ",rgb)
    cv2.waitKey(0)
    rgbs.append(rgb)

  return rgbs


def calibrate_camera(images):
  #ref - https://learnopencv.com/camera-calibration-using-opencv/
  # Defining the dimensions of checkerboard
  CHECKERBOARD = (6,9)
  criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

  # Creating vector to store vectors of 3D points for each checkerboard image
  objpoints = []
  # Creating vector to store vectors of 2D points for each checkerboard image
  imgpoints = [] 


  # Defining the world coordinates for 3D points
  objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
  objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
  prev_img_shape = None

  # Extracting path of individual image stored in a given directory
  #images = glob.glob('./images/*.jpg')
  for img in images:
      #img = cv2.imread(fname)
      gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
      # Find the chess board corners
      # If desired number of corners are found in the image then ret = true
      ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
      
      """
      If desired number of corner are detected,
      we refine the pixel coordinates and display 
      them on the images of checker board
      """
      if ret == True:
          objpoints.append(objp)
          # refining pixel coordinates for given 2d points.
          corners2 = cv2.cornerSubPix(gray, corners, (11,11),(-1,-1), criteria)
          
          imgpoints.append(corners2)

          # Draw and display the corners
          img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
      
      cv2.imshow('img',img)
      cv2.waitKey(0)

  cv2.destroyAllWindows()

  h,w = img.shape[:2]

  """
  Performing camera calibration by 
  passing the value of known 3D points (objpoints)
  and corresponding pixel coordinates of the 
  detected corners (imgpoints)
  """
  ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

  print("Camera matrix : \n")
  print(mtx)
  print("dist : \n")
  print(dist)
  print("rvecs : \n")
  print(rvecs)
  print("tvecs : \n")
  print(tvecs)

  intrinsics = {"fx":mtx[0,0],"fy":mtx[1,1],"cx":mtx[0,2],"cy":mtx[1,2]}
  return intrinsics



#read_extract_frames_from_movie()
calib_indices = [0,10,20,30,110,160]

images = load_verify_checkerboard_visibility(calib_indices)

intrinsics = calibrate_camera(images)
print("Got intrinsics ",intrinsics)


