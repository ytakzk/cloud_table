import torch
import torch.nn as nn
from torch.autograd import Variable
import numpy as np

class Encoder(nn.Module):

    def __init__(self):
        super(Encoder, self).__init__()
        
        self.conv1 = nn.Conv1d(3, 64, 1)
        self.conv2 = nn.Conv1d(64, 128, 1)
        self.conv3 = nn.Conv1d(128, 128, 1)
        self.conv4 = nn.Conv1d(128, 256, 1)
        self.conv5 = nn.Conv1d(256, 32, 1)
        self.maxPool1d = nn.MaxPool1d(2048)
        
        self.relu = nn.ReLU()
        self.bn1  = nn.BatchNorm1d(64) 
        self.bn2  = nn.BatchNorm1d(128) 
        self.bn3  = nn.BatchNorm1d(128)
        self.bn4  = nn.BatchNorm1d(256) 
        self.bn5  = nn.BatchNorm1d(32)

    def forward(self, x):

        x = self.relu(self.bn1(self.conv1(x)))
        x = self.relu(self.bn2(self.conv2(x)))
        x = self.relu(self.bn3(self.conv3(x)))
        x = self.relu(self.bn4(self.conv4(x)))
        x = self.relu(self.bn5(self.conv5(x)))
        x = torch.max(x, 2, keepdim=True)[0]#self.maxPool1d(x)
        return x


class Decoder(nn.Module):

    def __init__(self):
        super(Decoder, self).__init__()

        self.fc1 = nn.Linear(32, 256)
        self.fc2 = nn.Linear(256, 256)
        self.fc3 = nn.Linear(256, 2048*3)

        self.relu = nn.ReLU()
        self.bn1  = nn.BatchNorm1d(256) 
        self.bn2  = nn.BatchNorm1d(256) 
        
    def forward(self, x):

        x = x.view(x.shape[0], -1)
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        
        x = x.view(-1, 3, 2048)
        
        return x


class AutoEncoder(nn.Module):
    
    def __init__(self):
        super(AutoEncoder, self).__init__()

        self.encoder = Encoder()
        self.decoder = Decoder()

    def forward(self, x):

        x = self.encoder(x)
        x = self.decoder(x)
        
        return x