import socket
import argparse

import controller
import json

parser = argparse.ArgumentParser(description='initial conditions')
parser.add_argument('-port', action='store', default='9999', type=int)
args = parser.parse_args()

TCP_IP = '127.0.0.1'
TCP_PORT = args.port
BUFFER_SIZE = 1024

print('Connection address:', TCP_IP, TCP_PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(10)
 
conn, addr = s.accept()

print('initialize controller')
controller.init()

while 1:

    data = conn.recv(BUFFER_SIZE)
    if not data: break

    string = data.decode('utf-8')
    print(string)

    arr = string.split('&')[0].split('__')
    key = arr[0]

    if key == 'fetch_data':
        
        index = int(arr[1])
        res = controller.fetch_data(index)
        conn.sendall(data)

    elif key == 'manipulate':

        params = {}
        diff_str = arr[1]
        for diff_vals in diff_str.split(','):
            vals = diff_vals.split(':')
            k = int(vals[0])
            d = float(vals[1])
            params[k] = d

        controller.manipulate(params)
        controller.generate_pointcloud()
        conn.sendall(data)

    elif key == 'generate_pointcloud':
        
        controller.generate_pointcloud()
        conn.sendall(data)

    elif key == 'generate_mesh':
        
        alpha = float(arr[1])
        controller.generate_mesh(alpha)
        conn.sendall(data)

    elif key == 'close':
        s.close()
        break    
    else:
        pass

    # print("received data:", data)
    # print("received key:", key)
