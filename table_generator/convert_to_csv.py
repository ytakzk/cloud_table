import pandas as pd
import numpy as np
from torch.utils.data import Dataset
import glob
from pyntcloud import PyntCloud

def load_ply(file_name):
    cloud = PyntCloud.from_file(file_name)
    return cloud.points.values
    
file_names = glob.glob('./data/04379243/*.ply')

point_clouds = []
for file_name in file_names:
    print(file_name)
    name = file_name.split('.')[1].split('\\')[1]
    points = load_ply(file_name)

    output_name = './data/csv/%s.csv' % name
    np.savetxt(output_name, points, delimiter=',', fmt='%.2f')