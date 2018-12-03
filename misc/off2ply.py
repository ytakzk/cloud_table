import glob
import pymesh

def convert(directory):

    file_names = []
    for file_name in glob.glob('./%s/*.off' % directory):
        name = file_name.split('/')[-1].split('.')[0]
        print(name)
        mesh = pymesh.load_mesh(file_name)
        print(mesh)
        pymesh.save_mesh('./output/%s/%s.ply' % (directory, name), mesh)

convert('train')
convert('test')