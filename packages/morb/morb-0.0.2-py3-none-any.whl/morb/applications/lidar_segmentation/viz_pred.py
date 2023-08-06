import numpy as np
import open3d as o3d


def show_pcd(pcds):
    vis = o3d.visualization.Visualizer()
    vis.create_window()

    for pcd in pcds:
        vis.add_geometry(pcd)
    # run visualizer main loop
    print("Press Q or Excape to exit")
    vis.run()
    vis.destroy_window()


if __name__ == '__main__':
    #nuscenes results
    #pcd = o3d.io.read_point_cloud("predictions/1.pcd") #212, 100,200

<<<<<<< HEAD
    #shapenet results
    show_idcs = [100,200,212,216,220]
    for idx in show_idcs:
        pcd = o3d.io.read_point_cloud("predictions_shapenet/"+str(idx)+".pcd") # 100, 200, 212, 216, 220

        
        show_pcd([pcd])
=======
    pcd = o3d.io.read_point_cloud("predictions/1.pcd") #212, 100,200
    show_pcd([pcd])
>>>>>>> a7b4bee (sync)
