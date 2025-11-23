import _thread
import socket

import uosc.client
import uosc.server

class OSCClient:
    def __init__(self, server_ip, server_port):
        # Create an Open Sound Control client.
        self._osc_client = uosc.client.Client(server_ip, server_port)
    
    def send(self, *path_value_pairs):
        if len(path_value_pairs) == 1:
            path_value_pairs = path_value_pairs[0]
            self._osc_client.send(path_value_pairs[0], path_value_pairs[1])
        elif len(path_value_pairs) > 1:
            # Build an OSC bundle.
            osc_bundle = uosc.client.Bundle()
            for path, value in path_value_pairs:
                osc_bundle.add(uosc.client.create_message(path, value))
            self._osc_client.send(osc_bundle)


class OSCServer:
    max_dgram_size = 1472
    
    def __init__(self, ip, port, dispatcher, threaded=False):
        # When Threaded is False, this method never returns.
        # When Threaded is True, the _poll() method is executed on the second CPU core
        # and the __init__() method returns.
        
        self._dispatcher = dispatcher
        
        # Create a DGRAM UDP socket
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1) 
        self._socket.bind((ip, port))
        
        if not threaded:
            self._poll()
        else:
            _thread.start_new_thread(self._poll, ()) # start thread
        
    def _poll(self):
        # This method continuously poll the socket. Hence, it never returns
        while True:
          data, addr = self._socket.recvfrom(self.max_dgram_size)
          uosc.server.handle_osc(data, addr, dispatch=self._dispatcher)
          
