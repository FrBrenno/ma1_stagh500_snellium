import serial
import serial.tools.list_ports
import time
import threading

import uC_Connection
from colors import bcolors


class uC_Monitor:
    def __init__(self, baudrate=9600, MONITORING_PERIOD=.5, NO_ACTIVITY_THRESHOLD=20):
        self.MONITORING_PERIOD = MONITORING_PERIOD
        self.NO_ACTIVITY_THRESHOLD = NO_ACTIVITY_THRESHOLD
        self.baudrate = baudrate
        self.port_list = set()
        self.uC_port_list = set()
        self.is_monitoring = False
        self.no_port_activity_counter = 0
        
        self.monitor_thread = threading.Thread(target=self.monitor_ports)
        self.lock = threading.Lock()
        
    def is_uC_port(self, port):
        uC_connection = uC_Connection.uC_Connection(port, self.baudrate)
        return uC_connection.is_connected

    def start(self):
        if not self.is_monitoring:
            self.is_monitoring = True
            self.monitor_thread.start()
        
    def stop(self):
        self.is_monitoring = False
        self.monitor_thread.join()
        
    def monitor_ports(self):
        while self.is_monitoring:
            print("Monitoring ports...")
            current_port_list = set(serial.tools.list_ports.comports())
            new_ports = current_port_list - self.port_list
            
            self.lock.acquire()
            
            if len(new_ports) > 0: ## New ports found
                self.handle_new_ports(new_ports)
                
            elif len(new_ports) == 0: ## No new ports found
                self.handle_same_ports()
            
            if len(current_port_list) < len(self.port_list): ## Ports removed
                self.handle_removed_ports(self.port_list - current_port_list)
                
            self.port_list = current_port_list
            
            self.lock.release()
            time.sleep(self.MONITORING_PERIOD)
                
    def handle_new_ports(self, new_ports):
        for port in new_ports:
            print(f"Scanning port {port.device}")
            if self.is_uC_port(port.device):
                print(f"{bcolors.OKGREEN}uC found in port {port.device}{bcolors.ENDC}")
                self.uC_port_list.add(port.device)
                
    def handle_same_ports(self):
        print("No new ports found")
        if self.no_port_activity_counter > self.NO_ACTIVITY_THRESHOLD:
            print("No port activity detected for a while")
            print("Clearing uC port list")
            self.reset_port_lists()
            self.no_port_activity_counter = 0
        
        self.no_port_activity_counter += 1

    def reset_port_lists(self):
        # Keep uC ports and clear the rest
        self.port_list = self.uC_port_list.copy()    
    
    def handle_removed_ports(self, removed_ports):
        for port in removed_ports:
            print(f"{bcolors.FAIL}Port {port.device} removed{bcolors.ENDC}")
            if port.device in self.uC_port_list:
                self.uC_port_list.remove(port.device)
                print(f"uC removed from port {port.device}")
                
    def get_uC_ports(self):
        self.lock.acquire()
        uC_ports = self.uC_port_list.copy()
        self.lock.release()
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