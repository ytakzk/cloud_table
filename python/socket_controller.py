import time
import argparse
from subprocess import call
import torch
from torch.autograd import Variable
from lib.io import load_point_clouds, write_point_cloud
from lib.auto_encoder import Encoder, Decoder, AutoEncoder
import time

class Generator(AutoEncoder):
    
    def __init__(self, encoder, decoder):
        super(Generator, self).__init__()

        self.encoder = encoder
        self.decoder = decoder
        self.manipulator = {}

    def forward(self, x):

        x = self.encoder(x)

        # manipulation
        for key in self.manipulator:
            x[:,int(key),:] += self.manipulator[key]

        x = self.decoder(x)
        return x

def init():

    '''
    get trained models
    '''

    global encoder, decoder, generator

    encoder = Encoder()
    decoder = Decoder()

    encoder.load_state_dict(torch.load('../table_generator/models/encoder.pt', map_location={'cuda:0': 'cpu'}))
    decoder.load_state_dict(torch.load('../table_generator/models/decoder.pt', map_location={'cuda:0': 'cpu'}))
    
    generator = Generator(encoder, decoder)



def fetch_data(index):

    '''
    fetch data
    '''

    global point_clouds

    index_list = [index]
    point_clouds = load_point_clouds(index_list, directory='../table_generator/data/04379243')
    return 1


def manipulate(params):

    global generator_output

    '''
    manipulate its latent vector and get a new point cloud
    '''
    
    manipulator = {} 
    for key in params:
        manipulator[key] = params[key]

    generator.manipulator = manipulator
    generator_output = generator(point_clouds)

    return 1


def generate_pointcloud():

    '''
    write the point cloud into a file
    '''

    write_point_cloud(generator_output[0].detach().numpy(), '../pointcloud2mesh/mount/point_cloud.txt')
    return 1


def generate_mesh(alpha):

    '''
    call a c++ program to generate mesh
    '''

    command = '/cloud_table/pointcloud2mesh/build/pointcloud2mesh.out /cloud_table/pointcloud2mesh/mount/point_cloud.txt /cloud_table/pointcloud2mesh/mount/output.off %.5f' % alpha
    call(command.split(' '))
    return 1