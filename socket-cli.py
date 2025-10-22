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
        return self.socket.recv(buffer_size)
    def write(self, data):
        self.socket.send(data)
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        Debug(self.debug, "[SOCKET] Socket object exited.")
        self.close()

debug = 1 # activate debugging
buffer_size = 100
data = b''
with Socket(None, buffer_size, debug) as socket_obj: # will focus on the socket for interruption and closing
    socket_obj.open(("challenge01.root-me.org", 52002));

    while True:
        message = socket_obj.read(buffer_size)
        data += message
        if len(message) < buffer_size: # no more data to read
            break;
        
    data = data.decode("utf-8")
    print(data)
    
    matches = re.search(".*Calculate the square root of (?P<s1>\d*) and multiply by (?P<s2>\d*).*", data)
    s1 = int(matches.group('s1'))
    s2 = int(matches.group('s2'))
    square_root_of_s1 = int(math.sqrt(s1))
    res = square_root_of_s1 * s2
    print(res.to_bytes(res.bit_length(), 'big'))
    socket_obj.write(bytes(res))

    while True:
        message = socket_obj.read(buffer_size)
        data += message
        if len(message) < buffer_size: # no more data to read
            break;
        
    data = data.decode("utf-8")
    print(data)
