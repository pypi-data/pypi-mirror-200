import open3d as o3d
import numpy as np


def crop_fov(pcd, depth_cutoff = -6):
  #lidar generally gives a circle shaped pointcloud which covers 360 degree fov
  #but cameras have much limited fov
  #so using a depth cutoff value a segment of the pointcloud can be taken to reduce the fov of the lidar pointcloud

    points = np.array(pcd.points)
    colors = np.array(pcd.colors)
    

    n = points.shape[0]
    print("crop maxes ",np.max(points) )

    pcd_p = np.array(pcd.points).reshape((3,32,-1))
    pcd_c = np.array(pcd.colors).reshape((3,32,-1))
    print("shape of pcd points ",pcd_p.shape)


    n_cols = pcd_p.shape[2]
    
    #pcd_c[pcd_p[0,:,:]>20] = 0

    points_n = pcd_p.reshape((-1,3))
    colors_n = pcd_c.reshape((-1,3))


    colors_n[points_n[:,2]>depth_cutoff] = 0

    points_nn = []
    colors_nn = []

    for k in range(points_n.shape[0]):
        if points_n[k,2]<depth_cutoff:
            points_nn.append(points_n[k])
            colors_nn.append(colors_n[k])
    colors_nn = np.array(colors_nn)
    points_nn = np.array(points_nn)



    pcd_ = o3d.geometry.PointCloud()
    pcd_.points = o3d.utility.Vector3dVector(points_nn)
    pcd_.colors = o3d.utility.Vector3dVector(colors_nn)

    return pcd_

def sensor_alignment(pcd_, cs_record_lidar,pose_record_lidar, cs_record_cam, pose_record_cam):
  #transformation steps to align pointcloud to camera (roughly)
  #How to project lidar point cloud onto RGB frame ?
    # see lines 881 to 994 of below
    # https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/nuscenes.py#L642

    
    # First step: transform the pointcloud to the ego vehicle frame for the timestamp of the sweep.
    R = o3d.geometry.get_rotation_matrix_from_quaternion(np.array( cs_record_lidar['rotation']  ))
    pcd_ = pcd_.rotate(R, center=pcd_.get_center())
    T = np.eye(4)
    T[:-1, 3] = np.array(cs_record_lidar['translation'])
    pcd_ = pcd_.transform(T)


    # Second step: transform from ego to the global frame.
    R = o3d.geometry.get_rotation_matrix_from_quaternion(np.array( pose_record_lidar['rotation']  ))
    pcd_ = pcd_.rotate(R, center=pcd_.get_center())

    T = np.eye(4)
    T[:-1, 3] = np.array(pose_record_lidar['translation'])
    pcd_ = pcd_.transform(T)


    # Third step: transform from global into the ego vehicle frame for the timestamp of the image.
    T = np.eye(4)
    T[:-1, 3] = -np.array(pose_record_cam['translation'])
    pcd_ = pcd_.transform(T)

    R = o3d.geometry.get_rotation_matrix_from_quaternion(np.array( pose_record_cam['rotation']  ))
    pcd_ = pcd_.rotate(R.T, center=pcd_.get_center())



    # Fourth step: transform from ego into the camera.
    T = np.eye(4)
    T[:-1, 3] = -np.array(cs_record_cam['translation'])
    pcd_ = pcd_.transform(T)


    R = o3d.geometry.get_rotation_matrix_from_quaternion(np.array( cs_record_cam['rotation']  ))
    pcd_ = pcd_.rotate(R.T, center=pcd_.get_center())


    
    #180 degrees rotation
    R = pcd_.get_rotation_matrix_from_xyz((np.pi , 0, 0))
    pcd_ = pcd_.rotate(R, center=pcd_.get_center())

    return pcd_






def manual_align_pcd(pcd, filename = "view_point.json"):
    #using certain keypress (check out the keys from this func)
    #you can manually orient the pointcloud to precisely align with a provided RGB image


    def capture_depth(vis):
        depth = vis.capture_depth_float_buffer()
        #print("depth float buffer shape ",np.asarray(depth).shape)
        #print("sample ",np.unique(np.array(depth)))
        
        #cv2.imshow("capture buffer ",np.asarray(depth))
        #cv2.waitKey(0)
        cv2.imwrite("capture_depth_buffer.png",np.asarray(depth))
        return False


    def translate_view1(vis):
        ctr = vis.get_view_control()
        ctr.translate(1.0, 0.0)
        return False

    def translate_view2(vis):
        ctr = vis.get_view_control()
        ctr.translate(0.0, 1.0)
        return False

    def translate_view3(vis):
        ctr = vis.get_view_control()
        ctr.translate(-1.0, 0.0)
        return False

    def translate_view4(vis):
        ctr = vis.get_view_control()
        ctr.translate(0.0, -1.0)
        return False



    def rotate_view1(vis):
        ctr = vis.get_view_control()
        ctr.rotate(1.0, 0.0)
        return False

    def rotate_view2(vis):
        ctr = vis.get_view_control()
        ctr.rotate(0.0, 1.0)
        return False

    def rotate_view3(vis):
        ctr = vis.get_view_control()
        ctr.rotate(-1.0, 0.0)
        return False

    def rotate_view4(vis):
        ctr = vis.get_view_control()
        ctr.rotate(0.0, -1.0)
        return False





    def scale_view1(vis):
        ctr = vis.get_view_control()
        ctr.scale(-1.0001)
        return False
    def scale_view2(vis):
        ctr = vis.get_view_control()
        ctr.scale(1.0001)
        return False

    def change_fov1(vis):
        ctr = vis.get_view_control()
        ctr.change_field_of_view(step=0.01)
        return False
    def change_fov2(vis):
        ctr = vis.get_view_control()
        ctr.change_field_of_view(step=-0.01)
        return False

    def save_view(vis):
        param = vis.get_view_control().convert_to_pinhole_camera_parameters()
        o3d.io.write_pinhole_camera_parameters(filename, param)
        print("saved viewpoint extrinsic to ",filename)
        return False

    def load_view(vis):
        param = o3d.io.read_pinhole_camera_parameters(filename)
        ctr = vis.get_view_control()
        ctr.convert_from_pinhole_camera_parameters(param)
        return False




    key_to_callback = {}

    key_to_callback[ord("C")] = capture_depth

    key_to_callback[ord("W")] = translate_view4
    key_to_callback[ord("A")] = translate_view3
    key_to_callback[ord("S")] = translate_view2
    key_to_callback[ord("D")] = translate_view1

    key_to_callback[ord("U")] = rotate_view4
    key_to_callback[ord("H")] = rotate_view3
    key_to_callback[ord("J")] = rotate_view2
    key_to_callback[ord("K")] = rotate_view1


    key_to_callback[ord("O")] = scale_view1
    key_to_callback[ord("P")] = scale_view2

    key_to_callback[ord("N")] = change_fov1
    key_to_callback[ord("M")] = change_fov2


    key_to_callback[ord("V")] = save_view
    key_to_callback[ord("L")] = load_view

    o3d.visualization.draw_geometries_with_key_callbacks([pcd], key_to_callback, width=1600, height=900)



