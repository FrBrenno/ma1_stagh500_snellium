import serial
import serial.tools.list_ports
import pyudev

import uC_Connection
from colors import bcolors


class uC_Monitor:
    def __init__(self, baudrate=9600, init_event=False):
        self.baudrate = baudrate
        self.uC_port_list = set()
        self.is_monitoring = False
        self.init_event = init_event
        
        self.context = pyudev.Context()
        self.monitor = pyudev.Monitor.from_netlink(self.context)
        self.monitor.filter_by(subsystem='tty')
        self.observer = pyudev.MonitorObserver(self.monitor, self.device_event)
        
    def is_uC_port(self, port):
        uC_connection = uC_Connection.uC_Connection(port, self.baudrate)
        return uC_connection.is_connected

    def start(self):
        if not self.is_monitoring:
            self.is_monitoring = True
            self.scan_existing_ports()
            if self.init_event:
                self.init_event.set()
            self.observer.start()
            print("Started monitoring ports...")
        
    def stop(self):
        if self.is_monitoring:
            self.is_monitoring = False
            self.observer.stop()
            print("Stopped monitoring ports...")
    
    def scan_existing_ports(self):
        for port in serial.tools.list_ports.comports():
            self.handle_new_port(port.device)
    
    def handle_new_port(self, port):
        print(f"Scanning port {port}")
        if self.is_uC_port(port):
            self.uC_port_list.add(port)
            print(f"{bcolors.OKGREEN}uC found in port {port}{bcolors.ENDC}")  
    
    def handle_removed_port(self, port):
        self.uC_port_list.discard(port)
        print(f"{bcolors.FAIL}Port {port} removed{bcolors.ENDC}")

    def device_event(self, action, device):
        if action == 'add':
            self.handle_new_port(device.device_node)
        elif action == 'remove':
            self.handle_removed_port(device.device_node)
                
    def get_uC_ports(self):
        uC_ports = self.uC_port_list.copy()
        return uC_ports
                
if __name__ == "__main__":
    monitor = uC_Monitor()
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