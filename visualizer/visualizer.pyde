add_library('peasycam')
add_library('controlP5')

from dataset import Dataset
from decoder import Decoder
from socket_client import SocketClient
from gui import GUI

def gui_callback(key, value):
    
    global index, decoder
    
    if key == 'index':
        index = value
        dataset.fetch(value)
        socket_client.send('fetch_data__%d;&' % value)
        operation = 'manipulate__0:0;&'
        socket_client.send(operation)
        
    elif key == 'diff':
        
        decoder.fetched = False

def socket_callback(data):
    
    if not data:
        return
    
    print data

    if data.startswith('manipulate'):
        decoder.fetch()
        decoder.fetched = True

def setup():
    
    global dataset, decoder, socket_client, gui, cam, index
    
    size(1280, 720, P3D)
    fullScreen()

    cam = PeasyCam(this, width * 0.5, height * 0.5, 0, 100)
    gui = GUI(ControlP5(this), cam, gui_callback)
    
    zoomRatio = 0.25
    ortho(-width / 2*zoomRatio, width / 2*zoomRatio, -height / 2*zoomRatio, height / 2*zoomRatio, -1000, 1000)
    
    index = 0
    
    socket_client = SocketClient(socket_callback)
    dataset = Dataset()
    dataset.fetch(0)
    decoder = Decoder()
    decoder.fetch()
    socket_client.send('fetch_data__0;&')

    
def draw():
    
    background(0)
    translate(width * 0.5, height * 0.5)
    
    cam.setActive(not gui.is_operation() and mouseX < width - 145)
    
    if gui.out and not decoder.fetched:
        
        operation = 'manipulate__'
        for i, diff in enumerate(gui.diff_list):
            operation += '%d:%.3f,' % (i, diff)
        operation = operation[:-1] + ';&'
        
        socket_client.send(operation)
    
    if gui.in:
        dataset.draw()

    if gui.out:
        decoder.draw()

    gui.draw()
