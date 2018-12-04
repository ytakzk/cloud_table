import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset
from torch.autograd import Variable
import glob
from pyntcloud import PyntCloud

def load_ply(file_name):
    cloud = PyntCloud.from_file(file_name)
    return cloud.points.values

def load_obj(file_name):
    vertices = []
    with open(file_name) as f:
        for line in f:
            if line[:2] == 'v ':
                index1 = line.find(' ') + 1
                index2 = line.find(' ', index1 + 1)
                index3 = line.find(' ', index2 + 1)

                vertex = (float(line[index1:index2]), float(line[index2:index3]), float(line[index3:-1]))
                vertex = [round(vertex[0], 2), round(vertex[1], 2), round(vertex[2], 2)]
                vertices.append(np.array(vertex))
                
    return np.array(vertices)

def load_off(file_name):
    vertices = []
    with open(file_name) as f:
        for i, line in enumerate(f):
            vals = line.split(' ')
            if i > 2 and len(vals) == 3:
                vertex = [float(vals[0]), float(vals[1]), float(vals[2])]
                vertices.append(np.array(vertex))

    return np.random.permutation(np.array(vertices))[:2048]


class PointCloudDataset(Dataset):
    """Point cloud dataset."""

    def __init__(self, number=-1, directory='./data/04379243'):
        
        file_names = glob.glob('%s/*.ply' % directory)

        if number > 0 and len(file_names) > number:
            file_names = file_names[:number]
        
        point_clouds = []
        for file_name in file_names:

            points = load_ply(file_name)
            point_clouds.append(points)

        self.point_clouds = np.array(point_clouds, dtype='float64')
        self.point_clouds = np.transpose(self.point_clouds, (0, 2, 1))
        
    def __len__(self):
        return len(self.point_clouds)

    def __getitem__(self, idx):

        return self.point_clouds[idx]
    

def load_point_clouds(index_list, directory='./data/04379243'):
    
    file_names = glob.glob('%s/*.ply' % directory)

    point_clouds = []
    for i, file_name in enumerate(file_names):
        
        if i in index_list:
            points = load_ply(file_name)
            point_clouds.append(points)

    point_clouds = np.array(point_clouds, dtype='float64')
    point_clouds = np.transpose(point_clouds, (0, 2, 1))

    return Variable(torch.FloatTensor(point_clouds))


def write_point_cloud(points, file_path):
    
    if points.shape[0] < points.shape[1] and points.shape[0] == 3:
        points = points.T
    
    with open(file_path, 'w') as f:
        
        f.write(str(points.shape[0]) + '\n')

        for pt in points:
            f.write('%.8f %.8f %.8f\n' % tuple(pt))