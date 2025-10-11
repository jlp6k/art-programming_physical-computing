import network, socket, _thread


class AccessPoint:
    def __init__(self, ssid, password, activate=True, serve=True):
        """Configure the Pico W as a WiFi Access Point. 

        :param ssid: str, network SSID / name
        :param password: network password
        :param activate: bool, if True, starts the AP immediatly
        :param serve: bool, if True, starts the web server
        """
        # Create the Access Point network InterFace
        self._ap = network.WLAN(network.AP_IF)
        # Configure the network SSID / name and password 
        self._ap.config(essid=ssid, password=password)
        
        if activate:
            # Start the Access Point now
            self.active(True)
            
        if serve:
            # Start the web server on port 80
            # Create a STREAM TCP socket
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.bind(('', 80))
            self._socket.listen(5)
            
            # Start thread
            self._keep_server = True
            self._thread = _thread.start_new_thread(self._poll, ())

            
    def active(self, ena=None):
        """If a boolean argument is passed, activate or deactivate the network interface then
        returns the interface activation state.
        If no argument is provided, it just returns the interface state.
        """
        if ena is not None:
            self._ap.active(ena)
            
            # If activated, wait until the AP has started
            while self._ap.active() == False:
                pass    
        
        # Then return the current activation status
        return self._ap.active()
        
    @property
    def ip(self):
        """Return the AP IP address (as a string).
        """
        return self._ap.ipconfig('addr4')[0]
    
    @property
    def clients(self):
        """Returns a tuple byte strings corresponding to the MAC address of
        each client of the AP.
        """
        clients = self._ap.status('stations')
        if len(clients) > 0 and len(clients[0]) == 1:
            # The RSSI value is missing
            # at the moment, it's the case for the Pico W
            # Add a dummy RSSI
            clients = tuple([(mac[0], None) for mac in clients])
            
        return clients
    
    def _poll(self):
        while self._keep_server:
            # Accept / process an incoming connection
            conn, addr = self._socket.accept()
            # Get the query but don't do anything with it
            request = conn.recv(1024)
            
            # Build the page
            clients = "<p>"
            for mac, rssi in self.clients:
                # Build a MAC string xx:xx:xx:xx:xx:xx
                pretty_mac = ''
                # Take each byte of the MAC address
                for b in mac:
                    pretty_mac += f"{b:02x}:"
                pretty_mac = pretty_mac[:-1]

                clients += f"{pretty_mac} {rssi}<br/>"
            clients += "</p>"        
        
            response = f"""<html>
<head></head>
<body>
    <p>Connection received from {addr[0]}</p>
    <h3>Client list</h3>
    {clients}
    <p>Refresh the page to update the list</p>
</body>
</html>"""
            # Then send it back to the client
            conn.send(response)
            conn.close()
            
        # self._keep_server == False
        self._socket.close()
        

if __name__ == "__main__":
    import time
    
    # You must change that for security reason
    # Remember some OSes (like MacOS) need at least an 8 characters long password
    # otherwise they won't let the client join the AP.
    ssid = "PICO_AP"
    password = "password"
    
    # Instantiate an Access Point
    ap = AccessPoint(ssid, password)

    # If it's active (it should be) print a pretty message on the console
    if ap.active():
        print(f'Access Point is active ({ssid} / {password})')
        
        # The Access Point, which is probably at 192.168.4.1, waits for
        # HTTP requests, it will reply with a web page listing the WiFi clients
        # MAC addresses.
        print(f'Go to http://{ap.ip}/ to list the connected clients MAC addresses')
        
        # Don't quit now, things happen in the background
        while True:
            time.sleep(5)
    
    else:
        print("Something gone wrong. The Access Point isn't active!")
