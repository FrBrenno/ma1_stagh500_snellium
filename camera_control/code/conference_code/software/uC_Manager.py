import threading

from software.uC_Commands import PingCommand
from software.uC_Discoverer import uC_Discoverer


class uC_Manager:

    def __init__(self, baudrate=9600):
        self.baudrate = baudrate
        self.uC_connections = {}
        self.startup_sync = threading.Event()
        self.connections_lock = threading.Lock()
        self.uC_discoverer = uC_Discoverer(
            baudrate, self.uC_connections, self.connections_lock, self.startup_sync
        )

        self.monitor_thread = threading.Thread(target=self.uC_discoverer.start)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

        ## Event flag in order to synchronize the uC_Monitor start
        ## Wait for the uC_Monitor to start
        self.startup_sync.wait()

    def _retrieve_uC_connection(self, port):
        if port in self.uC_connections:
            return self.uC_connections[port]
        return None

    def connect_uC(self, port):
        self.connections_lock.acquire()
        connection = self._retrieve_uC_connection(port)
        self.connections_lock.release()

        if connection is None:
            print(f"Port {port} not available.")
            return False

        if not connection.is_connected:
            print(f"Connecting to port {port}...")
            connection.connect_to_port()
            if connection.is_connected:
                return True
            else:
                print("there2")
                print(f"Failed to connect to port {port}.")
                return False
        else:
            print(f"Already connected to port {port}.")
            return True

    def disconnect_uC(self, port):
        self.connections_lock.acquire()
        connection = self._retrieve_uC_connection(port)
        self.connections_lock.release()
        if connection is None:
            print(f"Port {port} not available.")
            return

        if connection.is_connected:
            connection.disconnect()
        print(f"Disconnected from port {port}.")

    def send_command_to_uC(self, command):
        self.connections_lock.acquire()
        if len(self.uC_connections) == 0:
            print("No uC available.")
            self.connections_lock.release()
            return None
        port = list(self.uC_connections.keys())[0]
        connection = self._retrieve_uC_connection(port)
        self.connections_lock.release()

        if connection is None:
            print(f"Port {port} not available.")
            return None
        
        for _ in range(3):
            if not connection.is_connected:
                connection.connect_to_port()
                if connection.is_connected:
                    break

        response = connection.send_command(command)
        return response

    def close(self):
        self.uC_discoverer.stop()
        for port in self.uC_connections:
            self.disconnect_uC(port)

    def print_uC_connections(self):
        """Prints the available uC connections."""
        for connection in self.uC_connections.values():
            print(connection)

    def get_uC_available(self):
        """Returns the available uC connections."""
        return self.uC_discoverer.get_uC_list()