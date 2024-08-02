import threading

import uC_monitor_events as uC_Monitor
import uC_Connection

class uC_Manager:
    """This class is responsible for managing the uC_Monitor and uC_Connection classes.
    """
    def __init__(self, baudrate=9600):
        self.baudrate = baudrate
        self.init_event = threading.Event()
        self.uC_monitor = uC_Monitor.uC_Monitor(baudrate, self.init_event)
        self.uC_connections = dict()
        
        self.monitor_thread = threading.Thread(target=self.uC_monitor.start)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        self.init_event.wait()
        
    def get_uC_ports(self):
        return self.uC_monitor.get_uC_ports()
    
    def connect_to_uC(self, port):
        if self.uC_monitor.is_uC_port(port):
            self.uC_connections[port] = uC_Connection.uC_Connection(port, self.baudrate)
            return True
        else:
            return False
        
    def disconnect_from_uC(self, port):
        if port in self.uC_connections:
            self.uC_connections[port].close()
            del self.uC_connections[port]
            return True
        else:
            return False
        
    def get_uC_connection(self, port):
        if port in self.uC_connections:
            return self.uC_connections[port]
        else:
            return None
        
    def get_uC_Connections(self):
        return self.uC_connections
        
    def close(self):
        self.uC_monitor.stop()
        for port in self.uC_connections:
            self.uC_connections[port].close()
        self.uC_connections.clear()
        
    
        
if __name__ == "__main__":
    manager = uC_Manager()
    selected_port = None
    command_to_send = None
    
    while True:
        # MENU : CONNECTION - COMMANDS - QUIT
        
        # CONNECTION : should show the available ports, the connected ports, the selected port to command
        print("#"*20)
        print("PORTS:")
        print("\tConnected:")
        for i, port in enumerate(manager.uC_connections):
            if port == selected_port:
                print(f"\t\t{i} {port} <---")
            else:
                print(f"\t\t{i} {port}")
            
        print("\tAvailable:")
        for j, port in enumerate(manager.get_uC_ports()):
            if port not in manager.uC_connections:
                print(f"\t\t{j} {port}")
                
                
        # COMMAND : should show command sent to the selected port and messages
        print("#"*20)
        print("COMMANDS:")
        if selected_port:
            print(f"\tSelected port: {selected_port}")
            if command_to_send:
                print(f"\tCommand to send: {command_to_send}")
                connection = manager.get_uC_connection(selected_port)
                print(f"\tMessages: \n{connection.send_command(command_to_send)}")
            else:
                print("\tNo command to send")
        
        # USER INPUT : select port, send command, quit
        print("#"*20)
        print("MENU:")
        print("\t1. Select port")
        print("\t2. Send command")
        print("\t3. Quit")
        
        usr_input = input("Enter option: ")
        if usr_input == "port":
            port = input("Enter port: ")
            if port in manager.get_uC_ports():
                selected_port = port
            else:
                print("Port not available")
        elif usr_input == "command":
            command = input("Enter command: ")
            command_to_send = command
        elif usr_input == "q":
            break
        
        
        
            

        
        
                
        
                
    manager.close()