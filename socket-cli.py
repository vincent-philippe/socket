import socket
import re
import math

class Debug:
    def __init__(self, debug : bool = False, message: str = None):
        if debug == True:
            print(message)

class Socket:
    ### * sock : A default socket to be used, otherwise a new one
    ### will be initialized with blocking behaviour as default
    ### * buffer_size : Is 100 for educationnal purpose
    ### * debug : If true, debug is activated, otherwise no debug would be shown
    def __init__(self, sock : socket.socket = None, buffer_size : int = 100, debug : bool = 0):
        if sock is None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.socket = sock
        self.debug = debug or 0
        self.buffer_size = buffer_size or 100
        Debug(self.debug, "[SOCKET] {0}".format(self.buffer_size))
        Debug(self.debug, "[SOCKET] Initialize a new socket object.")
    def open(self, socket_cnx: tuple[str, int]):
        self.socket.connect(socket_cnx)
        Debug(self.debug, "[SOCKET] Connexion OPEN... Waiting for read...")
    def close(self):
        self.socket.close()
        self.socket = None
        Debug(self.debug, "[SOCKET] Connexion was closed.")
    ###
    ### Return data as long as 'buffer_size' length (size in bytes).
    ### * buffer_size : The buffer size to read (in bytes) otherwise use the
    ### socket buffer_size defined in the constructor (default is 100 if not defined)
    ###
    def read(self, buffer_size : int = None):
        buffer_size = buffer_size or self.buffer_size
        Debug(self.debug, "[SOCKET] Reading {0} bytes of data...".format(buffer_size))
        d = self.socket.recv(buffer_size)
        Debug(self.debug, "[SOCKET-READ] {0}".format(d))
        return d
    def write(self, data):
        data = bytes(data + '\n', 'UTF-8', 'strict') # add EOL to stop server listening for data
        self.socket.send(data)
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        Debug(self.debug, "[SOCKET] Socket object exited.")
        self.close()

def get_server_data(socket_obj: socket.socket):
    data = b''
    while True:
        message = socket_obj.read(buffer_size)
        data += message
        if len(message) < buffer_size: # no more data to read
            break
    return data

def parse_and_compute_chal_solution(challenge):
    # extract challenge part
    matches = re.search(r".*Calculate the square root of (?P<s1>\d*) and multiply by (?P<s2>\d*).*", challenge.decode('UTF-8'))
    s1 = int(matches.group('s1'))
    s2 = int(matches.group('s2'))
    # proceed to compute parts as requested
    square_root_of_s1 = math.sqrt(s1)
    res = round(square_root_of_s1 * s2, 2)
    
    return res # return the result

def send_challenge_solution(socket: socket.socket, solution):
    solution = "{0}".format(solution)
    socket.write(solution)
    
debug = 0 # activate debugging
buffer_size = 1024
with Socket(None, buffer_size, debug) as socket_obj:
    socket_obj.open(("xxxxxxxxxxxxxxxx", 52002));
    c = get_server_data(socket_obj) # request server (will send challenge first)
    s = parse_and_compute_chal_solution(c)
    send_challenge_solution(socket_obj, s) # send solution
    flag = get_server_data(socket_obj)# get response
print(flag)
