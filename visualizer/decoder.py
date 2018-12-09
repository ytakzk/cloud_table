import os
import glob
import csv

class Decoder():
    
    def __init__(self, scale=100):
        
        self.scale = scale
        sep = '\\' if 'windows' in platformNames[this.platform].lower() else '/'         
        self.path = sep.join(sketchPath().split(sep)[:-1] + ['pointcloud2mesh', 'mount', 'point_cloud.txt'])      
        self.shape = None
        self.fetched = False

    def fetch(self):
        
        self.shape = createShape()
        self.shape.beginShape(POINTS)
        # self.shape.stroke(255)
        # self.shape.fill(255)
        self.shape.stroke(200, 70, 0)
        self.shape.fill(200, 70, 0)

        with open(self.path) as file:
            
            reader = csv.reader(file, delimiter=' ')
            
            for row in reader:
                
                if len(row) != 3:
                    continue
                self.shape.vertex(
                                  float(row[1]) * self.scale,
                                  float(row[2]) * -self.scale,
                                  float(row[0]) * self.scale)  
        self.shape.endShape()
        self.fetched =True

    def draw(self):
        
        if self.shape:
            shape(self.shape, 0, 0)
