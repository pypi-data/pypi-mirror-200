
annotated_data_folder = '/datasets/danfoss/lidar_person/supervisely_fake/' #containts subfolders img and ann which stores images as png and annotations as jsons respectively
train_folder = '/datasets/danfoss/lidar_person/' #here data will be accessed by the model during training
image_ext = '.png'


model_image_input_width = 512
model_input_image_height = 64
model_weights_path = "kpmodel"

#num_pred_regions = 28 #when the input image width to the model is 650
num_pred_regions = 21#when the input image width to the model is 512
use_median_prelayer = False

#always change this based on the dataset (the output of dataloaders/read_supervisely.py should give two numbers for max box width and height in the dataset)
#(use the highest values of that + 1)
max_bb_dim = 380.0


training_specific_w_downscale = 1 #what is the ratio of original width of image/model_image_input_width
training_specific_h_downscale = 1 #what is the ratio of original height of image/model_input_image_height

#these have to be adjusted carefully so that after the resize and the crop, the input to the model is (model_image_input_width, model_input_image_height)
training_specific_image_resize = (512,64)
training_specific_crop_w = [0,512]
training_specific_crop_h = [0,64]


#ouster scans provide range (channel 0), intensity and reflectivity  information , if you want to select a grayscaled version of all put -1
channel_selection = -1

#during inference, the projected lidar image may be processed to detect contours and supply the contour image to the model or just supply the plain image
test_image_preprocessing = "edge_detect" #options - "edge_detect" and "plain_read"

#folder from where to load up images from during testing model in inference
#test_images_folder = "/datasets/danfoss/lidar_person/supervisely_annotated/img/"
test_images_folder = "/datasets/lidar_post_detection/extracted_lidar_data/"

#this threshold is used to weed out false positives while visualizing model predictions
#default is 0.5, but is 1 is passed, then only predict the maximum confidence boxes
output_conf_thresh = 1.0

#sliding window moving average over model predictions (makes predictions smoother), can also pass None
#mvap = {"moving_window_size":5, "variance_capture": [15,15] }
mvap = None


#while displaying prediction output can crop the width and height in the ranges respectively, can also pass [] for no post processing
crop_pred_viz = [[256,512],[0,256]]