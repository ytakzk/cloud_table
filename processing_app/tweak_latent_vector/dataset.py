import os
import glob
import csv
import os

class Dataset():
    
    def __init__(self, scale=100):
        
        self.scale = scale
       
        root_dir = os.path.dirname(os.path.dirname(sketchPath()))

        file_template = os.sep.join([root_dir, 'data', '04379243_csv', '*'])

        self.paths = sorted(glob.glob(file_template))
        self.shape = None

    def fetch(self, index=0):
        
        self.shape = createShape()
        self.shape.beginShape(POINTS)
        self.shape.stroke(0, 90, 255)
        self.shape.fill(0, 90, 255)
        with open(self.paths[index]) as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:

                self.shape.vertex(
                                  float(row[1]) * self.scale,
                                  float(row[2]) * -self.scale,
                                  float(row[0]) * self.scale)  
        self.shape.endShape()
        
    def draw(self):
        
        shape(self.shape, 0, 0)
