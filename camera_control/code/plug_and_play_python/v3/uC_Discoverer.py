from colors import bcolors
from .uC_Connection import uC_Connection
from .uC_PortMonitor import uC_PortMonitor


class uC_Discoverer:
    def __init__(self, baudrate, uC_connections, lock, init_event=True):
        """
        Args:
            baudrate (int, optional): Baudrate of communication. Normally the baudrate decided by the uC Manager.
            init_event (bool, optional): Event flag to synchronize manager to monitor. Defaults to False.
        """
        self.baudrate = baudrate
        self.uC_connections = uC_connections
        self.is_monitoring = False
        self.connections_lock = lock
        self.init_event = init_event

        self.port_monitor = uC_PortMonitor(self, self.baudrate)

    def start(self):
        """Starts the monitoring of the ports."""
        if not self.is_monitoring:
            if self.init_event:
                self.port_monitor.scan_existing_ports()
                ## DEBUG PURPOSES
                if __name__ == "__main__":
                    ## For when running the script standalone
                    self.init_event = False
                else:
                    ## For when running the script as a module
                    self.init_event.set()
            self.port_monitor.start()
            self.is_monitoring = True

    def stop(self):
        """Stops the monitoring of the ports."""
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
            connection.disconnect()  # The connection is not needed, just for verification
            return connection
        return None

    def handle_new_port(self, port):
        """Handles the detection of a new port.
        It checks if the port is a uC port and adds it to the uC port list.
        """
        connection = self.is_uC_port(port)
        if connection:
            self.connections_lock.acquire()
            self.uC_connections[port] = connection
            self.connections_lock.release()

            print(f"{bcolors.OKGREEN}Port {port} added{bcolors.ENDC}")

    def handle_removed_port(self, port):
        """Handles the removal of a port.
        It removes the port from the uC port list.
        """
        if port in self.uC_connections:
            self.connections_lock.acquire()
            del self.uC_connections[port]
            self.connections_lock.release()
            
            print(f"{bcolors.FAIL}Port {port} removed{bcolors.ENDC}")

    def get_uC_list(self):
        """Returns a list of uC_Connection objects."""
        return list(self.uC_connections.values())


if __name__ == "__main__":
    connections = {}
    discoverer = uC_Discoverer(9600, connections)
    discoverer.start()
    while True:
        usr_input = input(
            f"{bcolors.OKBLUE}### Press Enter to get uC connections...{bcolors.ENDC}\n"
        )
        if usr_input == "":
            uC_list = discoverer.get_uC_list()
            if len(uC_list) > 0:
                print(f"{bcolors.OKBLUE}uC ports:")
                for uC in uC_list:
                    print("\t", uC)
            else:
                print(f"{bcolors.FAIL}No uC ports found{bcolors.ENDC}")
        else:
            break
    discoverer.stop()
    print("uC Monitor stopped")
