import serial
import serial.tools.list_ports
import pyudev

import uC_Connection
from colors import bcolors


class uC_Monitor:
    def __init__(self, baudrate=9600, init_event=False):
        """uC_Monitor class.
        Class to monitor the available ports and detect the uC ports.
        The class uses pyudev to monitor the ports and pyserial to detect the uC ports.
        

        Args:
            baudrate (int, optional): Baudrate of communication. Defaults to 9600.
            init_event (bool, optional): Event flag to synchronize manager to monitor. Defaults to False.
        """
        self.baudrate = baudrate
        self.uC_port_set = set()
        self.is_monitoring = False
        self.init_event = init_event
        
        self.context = pyudev.Context()
        self.monitor = pyudev.Monitor.from_netlink(self.context)
        self.monitor.filter_by(subsystem='tty')
        self.observer = pyudev.MonitorObserver(self.monitor, self.device_event)
        
    def is_uC_port(self, port):
        """Checks if the port is a uC port.
        It uses the uC_Connection class to check if the port is a uC port.
        """
        uC_connection = uC_Connection.uC_Connection(port, self.baudrate)
        return uC_connection.is_connected

    def start(self):
        """Starts the monitoring of the ports.
        """
        if not self.is_monitoring:
            print("Started monitoring ports...")
            self.is_monitoring = True
            ## Scan existing ports
            self.scan_existing_ports()
            if self.init_event:
                self.init_event.set()
                
            self.observer.start()
        
    def stop(self):
        """Stops the monitoring of the ports.
        """
        if self.is_monitoring:
            print("Stopped monitoring ports...")
            self.is_monitoring = False
            
            self.observer.stop()
    
    def scan_existing_ports(self):
        """Scans the existing ports to detect uC ports.
        It gets the list of ports and checks if they are uC ports.
        """
        for port in serial.tools.list_ports.comports():
            self.handle_new_port(port.device)
    
    def handle_new_port(self, port):
        """Handles the detection of a new port.
        It checks if the port is a uC port and adds it to the uC port list.
        """
        print(f"Scanning port {port}")
        if self.is_uC_port(port):
            self.uC_port_set.add(port)
            print(f"{bcolors.OKGREEN}uC found in port {port}{bcolors.ENDC}")  
    
    def handle_removed_port(self, port):
        """Handles the removal of a port.
        It removes the port from the uC port list.
        """
        self.uC_port_set.discard(port)
        print(f"{bcolors.FAIL}Port {port} removed{bcolors.ENDC}")

    def device_event(self, action, device):
        """Callback function for the device event.
        It calls the handle_new_port or handle_removed_port functions based on the action.
        """
        if action == 'add':
            self.handle_new_port(device.device_node)
        elif action == 'remove':
            self.handle_removed_port(device.device_node)
                
    def get_uC_ports(self):
        """Returns the list of uC ports.
        """
        return self.uC_port_set
                
if __name__ == "__main__":
    monitor = uC_Monitor()
    print(serial.tools.list_ports.comports())   
    monitor.start()
    while True:
        usr_input = input(f"{bcolors.OKBLUE}### Press Enter to get uC ports...{bcolors.ENDC}\n")
        if usr_input == "":
            uC_ports = monitor.get_uC_ports()
            if len(uC_ports) > 0:
                print(f"{bcolors.OKBLUE}uC ports: {uC_ports}{bcolors.ENDC}")
            else:
                print(f"{bcolors.FAIL}No uC ports found{bcolors.ENDC}")
        else:
            break
    monitor.stop()
    print("uC Monitor stopped")