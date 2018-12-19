import pandas as pd
import numpy as np
from torch.utils.data import Dataset
import glob
from pyntcloud import PyntCloud
import os


def load_ply(file_name):
    cloud = PyntCloud.from_file(file_name)
    return cloud.points.values
    
file_names = glob.glob('../mount/04379243/*.ply')

point_clouds = []
i = 0
for file_name in file_names:

    points = load_ply(file_name)

    output_name = file_name.replace('04379243', '04379243_csv').replace('.ply', '.csv')
    print(i, output_name)
    i += 1
    np.savetxt(output_name, points, delimiter=',', fmt='%.4f')
