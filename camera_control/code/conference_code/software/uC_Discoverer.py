from software.colors import bcolors
from software.uC_Connection import uC_Connection
from software.uC_PortMonitor import uC_PortMonitor


class uC_Discoverer:
    def __init__(self, baudrate, uC_connections, lock, init_event=True):
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
        if self.is_monitoring:
            self.port_monitor.stop()
            self.is_monitoring = False

    def is_uC_port(self, port):
        connection = uC_Connection(port, self.baudrate)
        if connection.is_connected:
            connection.disconnect()  # The connection is not needed, just for verification
            return connection
        return None

    def handle_new_port(self, port):
        connection = self.is_uC_port(port)
        if connection:
            self.connections_lock.acquire()
            self.uC_connections[port] = connection
            self.connections_lock.release()

            print(f"{bcolors.OKGREEN}Port {port} added{bcolors.ENDC}")

    def handle_removed_port(self, port):
        if port in self.uC_connections:
            self.connections_lock.acquire()
            del self.uC_connections[port]
            self.connections_lock.release()
            
            print(f"{bcolors.FAIL}Port {port} removed{bcolors.ENDC}")

    def get_uC_list(self):
        return list(self.uC_connections.values())