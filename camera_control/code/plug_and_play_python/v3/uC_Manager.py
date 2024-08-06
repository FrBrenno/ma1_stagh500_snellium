import threading

from uC_Discoverer import uC_Discoverer
from uC_Connection import uC_Connection

class uC_Manager:
    """This class is responsible for managin uC_Connection classes.
    It uses uC_Monitor to scan for available ports and uC_Connection to connect to the ports.
    """
    def __init__(self, baudrate=9600):
        """Initializes the uC_Manager class. 
        It creates a uC_Monitor object to scan for available ports.
        It also creates a dictionary to store uC_Connection objects.
        The uC_Connection objects are created when a port is selected.
        Args:
            baudrate (int, optional): baudrate of communication. Defaults to 9600.
        """
        self.baudrate = baudrate
        self.init_event = threading.Event()
        self.uC_discoverer = uC_Discoverer(baudrate, self.init_event)
        self.uC_connections = dict()
        
        self.monitor_thread = threading.Thread(target=self.uC_discoverer.start)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        ## Event flag in order to synchronize the uC_Monitor start
        ## Wait for the uC_Monitor to start
        self.init_event.wait()
        
    def get_uC_ports(self):
        """Returns the list of available ports.
        """
        return list(self.uC_discoverer.get_uC_ports())
    
    def connect_to_uC(self, port):
        """Connects to the uC port.
        Creates a uC_Connection object and stores it in the uC_connections dictionary.
        """
        self.uC_connections[port] = uC_Connection(port, self.baudrate)
        if self.uC_connections[port].is_connected:
            return True
        else:
            del self.uC_connections[port]
            return False
        
    def disconnect_from_uC(self, port):
        """Disconnects from the uC port.
        Closes the uC_Connection object and removes it from the uC_connections dictionary.
        """
        if port in self.uC_connections:
            self.uC_connections[port].disconnect()
            del self.uC_connections[port]
            return True
        else:
            return False
        
    def get_uC_connection(self, port):
        """Returns the uC_Connection object of the selected port.
        """
        if port in self.uC_connections:
            return self.uC_connections[port]
        else:
            return None
        
    def get_list_uC_Connections(self):
        """Returns the uC_Connection objects of all the connected ports.
        """
        return self.uC_connections
        
    def close(self):
        """Closes the uC_Manager class.
        Stops the uC_Monitor and disconnects from all the connected ports.
        """
        self.uC_discoverer.stop()
        for port in self.uC_connections:
            self.uC_connections[port].disconnect()
        self.uC_connections.clear()
    
            
if __name__ == "__main__":
    from uC_Commands import *
    
    print("Creating manager...")
    manager = uC_Manager()
    
    ports = manager.get_uC_ports()
    print(f"Available ports:")
    for i, port in enumerate(ports):
        print(f"{i+1}. {port}")
    print()
    
    print("Connecting to port 1...")
    manager.connect_to_uC(ports[0])
    
    connections = manager.get_list_uC_Connections()
    print(f"Connected ports:")
    for port in connections:
        print(f"{port}: {str(connections[port])}")
    print()    
    
    print("Sending command to port 1...")
    connection = manager.get_uC_connection(ports[0])
    connection.send_command(InfoCommand(), do_print=True)
    connection.send_command(PingCommand(), do_print=True)
    connection.send_command(TriggerCommand(), do_print=True)
    connection.send_command(TriggerCommand("select", 1, 3, 5), do_print=True) 
    
    
    print("Disconnecting from port 1...")
    manager.disconnect_from_uC(ports[0])
    
    connections = manager.get_list_uC_Connections()
    print(f"Connected ports:")
    for port in connections:
        print(f"{port}: {connections[port]}")         
    print()
    
    print("Closing manager...")
    manager.close()