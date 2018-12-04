import 

import glob
from pyntcloud import PyntCloud

import torch
import torch.nn as nn
from torch.autograd import Variable
from torch.utils.data import Dataset, DataLoader

import numpy as np

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

point_cloud_dataset = PointCloudDataset(8) #8480
dataloader = DataLoader(point_cloud_dataset, batch_size=8, shuffle=True)


class Generator(AutoEncoder):
    
    def __init__(self, encoder, decoder):
        super(AutoEncoder, self).__init__()

        self.encoder = encoder
        self.decoder = decoder

    def forward(self, x):

        x = self.encoder(x)
        x = self.decoder(x)        
        return x


v_encoder = Encoder()
v_decoder = Decoder()

v_encoder.load_state_dict(torch.load('./models/encoder.pt'))
v_decoder.load_state_dict(torch.load('./models/decoder.pt'))

train_input  = next(iter(dataloader)).float()

generator = Generator(v_encoder, v_decoder)
generator_output = generator(train_input)
