import machine, network, socket, _thread, time, binascii


class AccessPoint:
    def __init__(self, ssid, password, activate=True, serve=False):
        """Configure the Pico W as a Client Access Point.

        If the serve optional parameter is True, the instance creates an HTTP server
        that replies to requests with a page listing the MAC addresses of the connected
        Client clients.

        :param ssid: str, network SSID / name
        :param password: network password
        :param activate: bool, if True, starts the AP immediately
        :param serve: bool, if True, starts the web server
        """
        # Create the Access Point network InterFace
        self._ap = network.WLAN(network.AP_IF)
        # Configure the network SSID / name and password 
        self._ap.config(essid=ssid, password=password)
        
        if activate:
            # Start the Access Point now
            self.active(True)

        self._serve = serve
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
            while not self._ap.active():
                pass
        
        # Then return the current activation status
        return self._ap.active()
        
    @property
    def serve(self):
        return self._serve

    @property
    def mac(self):
        return binascii.hexlify(self._ap.config('mac'), ':').decode()

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
            clients = """
<table>
  <thead>
    <tr><th scope="col">#</th><th scope="col">MAC address</th><th scope="col">RSSI</th></tr>
  </thead>
  <tbody>
"""
            for c, (mac, rssi) in enumerate(self.clients):
                # Build a MAC string xx:xx:xx:xx:xx:xx
                pretty_mac = ''
                # Take each byte of the MAC address
                for b in mac:
                    pretty_mac += f"{b:02x}:"
                pretty_mac = pretty_mac[:-1]

                if rssi is not None:
                    clients += f"<tr><td>{c+1:02}</td><td>{pretty_mac}</td><td>{rssi}</td></tr>\n"
                else:
                    clients += f"<td>{c+1:02}</td><td>{pretty_mac}</td><td></td>\n"
            clients += """
  </tbody>
</table>
"""

            #
            response = f"""<html>
<head>
  <style>
table {{
  border: 2px solid rgb(140 140 140);
}}

th,
td {{
  border: 1px solid rgb(160 160 160);
}}
  </style>
</head>
<body>
    <p>The access point MAC address is {self.mac}</p>
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


class Client:
    TRACE_NONE = 0
    TRACE_MAC_ADDR = 1
    TRACE_IP_ADDR = 2
    TRACE_SCAN_ONCE = 4
    TRACE_SCAN_CONTINUOUS = 8
    TRACE_CONNECTION = 16
    TRACE_ALL = TRACE_MAC_ADDR | TRACE_IP_ADDR | TRACE_SCAN_CONTINUOUS | TRACE_CONNECTION

    _status_strings = {-3: "Authentication failed",
                       -2: "No matching SSID found (could be out of range, or down)",
                       -1: "Connection failed",
                       0: "Link is down",
                       1: "Connection in progress",
                       2: "Connection in progress, waiting for an IP address",
                       3: "The connection was established successfully"}

    def __init__(self, ssid, password, retries=-1, traces=TRACE_NONE, blink_led=False, max_power=True):
        """Initialize a WiFi client connection.

        :param ssid: str, network SSID / name
        :param password: str, network password
        :param retries: int, while connecting to a WiFi network, number of retries
        :param traces: int, the kind of traces to display
        :param blink_led: bool, if True blink LED to report connection progress
        :param max_power: bool, if True set the WiFi power to the maximum otherwise reduce power consumption
        """
        self._ssid = ssid

        if blink_led:
            # Initialize status LED
            self._status_led = machine.Pin('WL_GPIO0', machine.Pin.OUT)
            self._status_led.off()

        # Create the network interface
        self._wlan = network.WLAN(network.STA_IF)

        if max_power:
            # Set maximum power (i.e. disable power savings)
            self._wlan.config(pm=network.WLAN.PM_PERFORMANCE)
            # Another way to unset power saving mode
            # See: https://datasheets.raspberrypi.com/picow/connecting-to-the-internet-with-pico-w.pdf
            self._wlan.config(pm=0xa11140)
            # Not sure any of these actually work!

        # Activate the interface
        self._wlan.active(True)

        if traces & Client.TRACE_MAC_ADDR:
            print(f"MAC address: {self.mac}\n")

        if traces & Client.TRACE_SCAN_ONCE or traces & Client.TRACE_SCAN_CONTINUOUS:
            self.__class__._print_scan(self._wlan)
            print()

        last_status = None
        while True:
            # The loop is exited
            #    if the number of retries reaches 0 (this won't occur by default)
            #    if last_status is positive or None

            if traces & Client.TRACE_CONNECTION:
                print("Connecting SSID:", ssid, end='')

            # Try to connect
            self._wlan.connect(ssid, password)

            while not self._wlan.isconnected():
                # The inner loop / connection retry loop is exited if it's connected or the status is <= 0

                # Get interface status
                status = self._wlan.status()

                if traces & Client.TRACE_CONNECTION:
                    # If status has changed
                    if status != last_status:
                        print(f"\nStatus: {self.__class__._status_strings.get(status, '?')}", end='')
                    else:
                        # Status didn't change, print a . to show it's running
                        print(f".", end='')

                last_status = status

                # If things went wrong, try to restart the connection process from the beginning
                # by leaving the inner loop
                if status <= 0:
                    break

                # Wait for a while
                time.sleep(1)

                if blink_led:
                    self._status_led.toggle()

                # Stay in this inner loop until it's connected or something gone wrong (status <= 0)

            # Check if the interface is connected,
            # and if it's the case, exit the loop
            if last_status is None or last_status > 0:
                if blink_led:
                    self._status_led.on()
                break

            # If the retry count has reached 0, exit the loop
            if retries == 0:
                break

            # Decrease retries
            retries -= 1

            # Let's retry to reconnect, toggle the interface on/off/on
            if traces & Client.TRACE_CONNECTION:
                print("\nResetting", end='')

            # Deactivate interface
            self._wlan.active(False)

            # Wait 5 seconds
            for i in range(20):
                time.sleep(0.25)
                if traces & Client.TRACE_CONNECTION and ((i % 4) == 0):
                    print(f".", end='')
                if blink_led:
                    self._status_led.toggle()
            print("\n")

            # Reactivate interface
            self._wlan.active(True)

            if traces & Client.TRACE_SCAN_CONTINUOUS:
                self._print_scan(self._wlan)
                print()

            # End of the outer connection loop

        if traces & Client.TRACE_CONNECTION:
            print("\n")

        if traces & Client.TRACE_IP_ADDR:
            print(f"IP address: {self.ip}{' (connection failed)' if not self._wlan.isconnected() else ''}")

        if blink_led and self._status_led.value() == 1:
            self._status_led.off()

    @property
    def wlan(self):
        return self._wlan

    @property
    def mac(self):
        return binascii.hexlify(self._wlan.config('mac'), ':').decode()

    @property
    def ip(self):
        if self._wlan.isconnected():
            return self._wlan.ifconfig()[0]
        return None

    @property
    def ssid(self):
        return self._ssid

    def isconnected(self):
        return self._wlan.isconnected()

    @staticmethod
    def scan():
        """The scan() method scans the available Client networks and prints a report.
        """
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)

        mac_address = binascii.hexlify(wlan.config('mac'), ':').decode()

        print(f"Mac address: {mac_address}")
        print()

        Client._print_scan(wlan)

    @staticmethod
    def _print_scan(wlan):
        security_strings = {0: "open", 1: "WEP", 2: "WPA-PSK", 3: "WPA2-PSK", 4: "WPA/WPA2-PSK", 5:"WPA3-PSK", 7:"WPA/WPA2-PSK"}

        # self._wlan.scan() returns a list of tuples, each tuple contains 6 values:
        # 0: SSID name of the received network
        # 1: bSSID id of the received access point
        # 2: channel Client channel
        # 3: RSSI power of the incoming signal
        # 4: security type of encryption
        # 5: visibility of the SSID
        # Sort the list by RSSI
        received_networks = sorted(wlan.scan(), key=lambda x: x[3], reverse=True)  # sorted on RSSI (3)

        print(f"  |{'available SSID':18}|{'BSSID':12}|{'chan':4}|{'RSSI (dBm)':10}|{'security':14}|{'hidden':6}")
        print(f"--+{'-' * 18}+{'-' * 12}+{'-' * 4}+{'-' * 10}+{'-' * 14}+{'-' * 6}")

        i = 0
        for w in received_networks:
            i += 1
            ssid = w[0].decode() if w[0][0] != 0 else ' '
            print(f"{i:2d}|{ssid:18}|{binascii.hexlify(w[1]).decode():12}|{w[2]:4}|{w[3]:10}|{w[4]:1}:"
                  f"{security_strings.get(w[4], ''):12}|{w[5]:6}")


def access_point_demo():
    """The access_point_demo() function creates a Client Access Point. The network name is PICO_AP, and
    the password is password. If you plan to reuse this code you must change those values for security reason.

    Remember some OSes (like MacOS) need at least an 8 characters long password otherwise they won't
    let the client join the AP.
    """
    ssid = "PICO_AP"
    password = "password"

    # Instantiate an Access Point
    ap = AccessPoint(ssid, password, serve=True)

    # Print Access Point MAC address
    print(f"Access Point MAC address / BSSID: {ap.mac}\n")

    # If it's active (it should be) print a pretty message on the console
    if ap.active():
        print(f'Access Point is active ({ssid} / {password})')

        if ap.serve:
            # The Access Point, which is probably at 192.168.4.1, waits for
            # HTTP requests, it will reply with a web page listing the clients
            # MAC addresses.
            print(f'Go to http://{ap.ip}/ to list the connected clients MAC addresses')

            # Don't quit now, things happen in the background
            while True:
                time.sleep(5)

    else:
        print("Something gone wrong. The Access Point isn't active!")


def scan_demo():
    while True:
        Client.scan()
        print()
        time.sleep(10)

if __name__ == "__main__":
    access_point_demo()
    # scan_demo()
    # Client("PICO_AP", "password", traces=Client.TRACE_ALL, blink_led=True, retries=2)
