import time
import argparse
from subprocess import call
import torch
from torch.autograd import Variable
from lib.io import load_point_clouds, write_point_cloud, load_same_point_clouds
from lib.auto_encoder import Encoder, Decoder, AutoEncoder
import time
import numpy as np
import json
import pandas as pd
import csv

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


def fetch_point_clouds(index):

    '''
    fetch point clouds
    '''

    global point_clouds

    index_list = [i for i in range(index)]
    point_clouds = load_point_clouds(index_list, directory='../table_generator/data/04379243')

    point_clouds = point_clouds.detach().numpy()
    print(point_clouds.shape)
    return np.swapaxes(point_clouds, 2, 1).tolist()


def create_weather_table(time_index=5):

    '''
    create_weather_table
    '''

    global point_clouds

    id_list = [2352778, 3451138, 3941584, 3451189, 188714, 587084, 1496153, 1311874, 2643743, 5128638, 1850147, 1275339, 2657896, 5368361, 3369157, 360630, 184745, 1796236, 1880251, 2147714] 

    # input data
    point_clouds = load_same_point_clouds(10, len(id_list), directory='../table_generator/data/04379243')

    # location data
    f = open('./data/cities.json')
    cities = json.load(f)
    f.close()
    places = []
    for id in id_list:
        
        for c in cities:
            
            if c['id'] == id:
                c['name'] = c['name'].upper()
                places.append(c)
                break

    # weather data
    df = pd.read_pickle('./data/weather.pkl')
    df.head()
    df_std = (df - df.mean()) / df.std() * 0.1
    df_std.head()
    index = df.query('time_index==%d' % time_index).index
    manupulation_values = df_std.iloc[index, :].as_matrix()

    weather_code_dic = {}
    with open('./data/weather_codes.csv') as f:
        
        lines = csv.reader(f)
        
        for l in lines:    
            weather_code_dic[l[0]] = l[1]

    weather_str = []
    for id in df['weather_id']:
        string = weather_code_dic[str(id)].upper()
        weather_str.append(string)
    
    df['weather_str'] = weather_str

    weather_values = df.iloc[index, :].reset_index().to_json()

    letent_vector = encoder(point_clouds)

    vectors = []
    for i in range(len(id_list)):
        values = manupulation_values[i]
        for j in range(len(values)):
            print(letent_vector[i][j], values[j])
            letent_vector[i][j] += values[j]
    output = decoder(letent_vector)
    output = output.detach().numpy()

    return np.swapaxes(output, 2, 1).tolist(), places, weather_values


def manipulate(data):

    global generator_output

    '''
    manipulate its latent vector and get a new point cloud
    '''

    x1 = np.array(data['x1'])
    y1 = np.array(data['y1'])
    z1 = np.array(data['z1'])

    x2 = np.array(data['x2'])
    y2 = np.array(data['y2'])
    z2 = np.array(data['z2'])

    pc1 = np.array([x1, y1, z1])
    pc2 = np.array([x2, y2, z2])

    alpha = float(data['alpha'])

    point_clouds  = np.array([pc1, pc2])

    letent_vector = encoder(Variable(torch.FloatTensor(point_clouds)))

    num = 6

    vectors = []
    for i in range(6):
        alpha = i * (1.0 / (num - 1))
        vec = letent_vector[0] * (1.0 - alpha) + letent_vector[1] * alpha
        vec = vec.unsqueeze(0)
        vectors.append(vec)
    merged_letent_vector = torch.cat(vectors, dim=0)
    output = decoder(merged_letent_vector)
    output = output.detach().numpy()

    return np.swapaxes(output, 2, 1).tolist()


def generate_pointcloud():

    '''
    write the point cloud into a file
    '''

    write_point_cloud(generator_output[0].detach().numpy(), '../pointcloud2mesh/mount/point_cloud.txt')
    return 1


def generate_mesh(data, alpha=0.0):

    '''
    call a c++ program to generate mesh
    '''

    x = np.array(data['x'])
    y = np.array(data['y'])
    z = np.array(data['z'])

    pc = np.array([x, y, z])
    write_point_cloud(pc, '../pointcloud2mesh/mount/point_cloud.txt')

    command = '/cloud_table/pointcloud2mesh/build/pointcloud2mesh.out /cloud_table/pointcloud2mesh/mount/point_cloud.txt /cloud_table/pointcloud2mesh/mount/output.off %.5f' % alpha
    call(command.split(' '))

    file = open('../pointcloud2mesh/mount/output.off', 'r')

    return file.read()
