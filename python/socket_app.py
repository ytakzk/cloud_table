import socket
import socket_controller as controller
import json

TCP_IP = '0.0.0.0'
TCP_PORT = 9998
BUFFER_SIZE = 1024

print('Connection address:', TCP_IP, TCP_PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(10)
 
conn, addr = s.accept()

print('initialize controller')
controller.init()

def run(operation):

    if len(operation) == 0 or operation[-1] != ';':
        return True

    operation = operation[:-1]

    arr = operation.split('__')
 
    key = arr[0]

    if key == 'fetch_data':
        
        index = int(arr[1])
        res = controller.fetch_data(index)
        conn.sendall(operation.encode())

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
        conn.sendall(operation.encode())

    elif key == 'generate_pointcloud':
        
        controller.generate_pointcloud()
        conn.sendall(operation.encode())

    elif key == 'generate_mesh':
        
        alpha = float(arr[1])
        controller.generate_mesh(alpha)
        conn.sendall(operation.encode())

    elif key == 'close':
        s.close()
        return False    
    else:
        pass

    return True

while 1:

    data = conn.recv(BUFFER_SIZE)
    if not data: break

    string = data.decode('utf-8')
    print(string)

    arr = string.split('&')
    
    for o in arr:
        run(o)