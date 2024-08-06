from uC_PortMonitor import uC_PortMonitor
from uC_Connection import uC_Connection
from colors import bcolors

class uC_Discoverer:
    def __init__(self, baudrate=9600, init_event=False):
        """uC_Monitor class.
        Class to monitor the available ports and detect the uC ports.
        The class uses pyudev to monitor the ports and pyserial to detect the uC ports.
        

        Args:
            baudrate (int, optional): Baudrate of communication. Defaults to 9600.
            init_event (bool, optional): Event flag to synchronize manager to monitor. Defaults to False.
        """
        self.baudrate = baudrate
        self.uC_connections = {}
        self.is_monitoring = False
        self.init_event = init_event
        
        self.port_monitor = uC_PortMonitor(self, self.baudrate)

    def start(self):
        """Starts the monitoring of the ports.
        """
        if not self.is_monitoring:
            if not self.init_event:
                self.port_monitor.scan_existing_ports()
                ##self.init_event.set()
            self.port_monitor.start()
            self.is_monitoring = True
        
    def stop(self):
        """Stops the monitoring of the ports.
        """
        if self.is_monitoring:
            self.port_monitor.stop()
            self.is_monitoring = False
    
    def is_uC_port(self, port):
        """Checks if the port is a uC port.
        It creates a uC_Connection object and tries to connect to the port.
        If the connection is successful, set it into the dictionay and return True.
        """
        connection = uC_Connection(port, self.baudrate)
        if connection.is_connected:
            connection.disconnect() # The connection is not needed, just for verification
            return connection
        return None
    
    def handle_new_port(self, port):
        """Handles the detection of a new port.
        It checks if the port is a uC port and adds it to the uC port list.
        """
        connection = self.is_uC_port(port)
        if connection:
            self.uC_connections[port] = connection
            print(f"{bcolors.OKGREEN}Port {port} added{bcolors.ENDC}")

    def handle_removed_port(self, port):
        """Handles the removal of a port.
        It removes the port from the uC port list.
        """
        if port in self.uC_connections:
            del self.uC_connections[port]
            print(f"{bcolors.FAIL}Port {port} removed{bcolors.ENDC}")
                
    def get_uC_ports(self):
        """Returns the list of uC ports.
        """
        return list(self.uC_connections.keys())
    
    def get_uC_connections(self):
        """Returns the uC_Connection objects of all the connected ports.
        """
        return self.uC_connections
    
    def get_uC_connection(self, port):
        """Returns the uC_Connection object of the selected port.
        """
        if port in self.uC_connections:
            return self.uC_connections[port]
        else:
            return None
                
if __name__ == "__main__":
    discoverer = uC_Discoverer()
    discoverer.start()
    while True:
        usr_input = input(f"{bcolors.OKBLUE}### Press Enter to get uC ports...{bcolors.ENDC}\n")
        if usr_input == "":
            uC_ports = discoverer.get_uC_ports()
            if len(uC_ports) > 0:
                print(f"{bcolors.OKBLUE}uC ports: {uC_ports}{bcolors.ENDC}")
            else:
                print(f"{bcolors.FAIL}No uC ports found{bcolors.ENDC}")
        else:
            break
    discoverer.stop()
    print("uC Monitor stopped")