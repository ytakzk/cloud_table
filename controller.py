import time
import argparse
from subprocess import call
import torch
from torch.autograd import Variable
from table_generator.lib.io import load_point_clouds, write_point_cloud
from table_generator.lib.auto_encoder import Encoder, Decoder, AutoEncoder
import time

class Generator(AutoEncoder):
    
    def __init__(self, encoder, decoder):
        super(Generator, self).__init__()

        self.encoder = encoder
        self.decoder = decoder

    def forward(self, x):

        x = self.encoder(x)
        x = self.decoder(x)
        return x

def init():

    '''
    get trained models
    '''

    global encoder, decoder, generator

    encoder = Encoder()
    decoder = Decoder()

    encoder.load_state_dict(torch.load('./table_generator/models/encoder.pt'))
    decoder.load_state_dict(torch.load('./table_generator/models/decoder.pt'))
    
    generator = Generator(encoder, decoder)



def fetch_data(index):

    '''
    fetch data
    '''

    global point_clouds

    index_list = [index]
    point_clouds = load_point_clouds(index_list, directory='./table_generator/data/04379243')
    print(point_clouds.shape)
    return '1'


def manipulate():

    global generator_output

    '''
    manipulate its latent vector and get a new point cloud
    '''

    generator_output = generator(point_clouds)
    return '1'


def generate_mesh():

    '''
    write the point cloud into a file
    call a c++ program to generate mesh
    '''

    write_point_cloud(generator_output[0].detach().numpy(), './pointcloud2mesh/mount/point_cloud.txt')

    command = 'docker exec cgal /DeepTable/pointcloud2mesh/build/pointcloud2mesh.out ./mount/point_cloud.txt ./mount/output.off'
    call(command.split(' '))
    return '1'