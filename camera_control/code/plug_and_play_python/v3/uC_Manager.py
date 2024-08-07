import threading

from .uC_Commands import PingCommand
from .uC_Discoverer import uC_Discoverer


class uC_Manager:
    """This class is the interface for managing uC_Connections and issuing commands to the uC.
    It creates a uC_Discoverer object to scan for available ports.
    """

    def __init__(self, baudrate=9600):
        """Initializes the uC_Manager class.
        First, it creates a uC_Discoverer object to discover the uC ports and then, it is
        started in a separate thread. Thus, the uC_Manager waits for the uC_Discoverer to
        start before allowing the user to issue commands.

        Args:
            baudrate (int, optional): baudrate of communication. Defaults to 9600.
        """
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

    def get_uC_connection(self, port):
        """Returns the uC connection by the port."""
        if port in self.uC_connections:
            return self.uC_connections[port]
        return None

    def connect_uC(self, port):
        """Connects to the uC by the port."""
        self.connections_lock.acquire()
        connection = self.get_uC_connection(port)
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
                print(f"Failed to connect to port {port}.")
                return False
        else:
            print(f"Already connected to port {port}.")
            return True

    def disconnect_uC(self, port):
        """Disconnects from the uC by the port."""
        self.connections_lock.acquire()
        connection = self.get_uC_connection(port)
        self.connections_lock.release()
        if connection is None:
            print(f"Port {port} not available.")
            return

        if connection.is_connected:
            connection.disconnect()
        print(f"Disconnected from port {port}.")

    def send_command_to_uC(self, port, command):
        """Sends a command to the uC by the port."""
        self.connections_lock.acquire()
        connection = self.get_uC_connection(port)
        self.connections_lock.release()
        if connection is None:
            print(f"Port {port} not available.")
            return None

        if connection.is_connected:
            return connection.send_command(command)
        print(f"Failed to send command to port {port}.")
        return None

    def close(self):
        """Closes the uC_Manager by stopping the uC_Discoverer and disconnecting all uC connections."""
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


if __name__ == "__main__":
    print("Creating manager...")
    manager = uC_Manager()

    while True:
        print("## Available ports:")
        manager.print_uC_connections()

        port = input("## Enter the port to connect (q to quit): ")
        if port == "q":
            break
        elif port not in manager.uC_connections:
            print("Port not available.", end="\n\n")
            continue
        else:
            print("\n" + "#" * 50, end="\n")

            print(f"## Connecting to port {port}...")
            manager.connect_uC(port)
            manager.print_uC_connections()

            print("## Sending command...")
            response = manager.send_command_to_uC(port, PingCommand())

            print("## Response:", response)

            print("## Disconnecting from port...")
            manager.disconnect_uC(port)

            print("#" * 50, end="\n")

    print("Closing manager...")
    manager.close()

    """ print("Connecting to port...")
    manager.connect_uC("/dev/ttyUSB0")
    manager.print_uC_connections()
    
    print("Sending command...")
    response = manager.send_command_to_uC("/dev/ttyUSB0", PingCommand())
    
    print("Response:", response)
    
    print("Disconnecting from port...")
    manager.disconnect_uC("/dev/ttyUSB0")
    manager.print_uC_connections()
    
    print("Closing manager...")
    manager.close()
    print("Manager closed.")  """
