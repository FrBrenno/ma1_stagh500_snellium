import pyudev
from serial.tools import list_ports

from uC_Connection import uC_Connection

class uC_PortMonitor:
    def __init__(self, discoverer, baudrate=9600):
        self.listener = discoverer
        self.baudrate = baudrate
        
        self.context = pyudev.Context()
        self.monitor = pyudev.Monitor.from_netlink(self.context)
        self.monitor.filter_by(subsystem='tty')
        self.observer = pyudev.MonitorObserver(self.monitor, self.device_event)

    def start(self):
        """Starts the monitoring of the ports.
        """
        self.observer.start()
        print("Started monitoring ports...")
        
    def stop(self):
        """Stops the monitoring of the ports.
        """
        self.observer.stop()
        print("Stopped monitoring ports...")
    
    def scan_existing_ports(self):
        """Scans the existing ports to detect uC ports.
        It gets the list of ports and checks if they are uC ports.
        """
        print("Scanning existing ports...")
        for port in list_ports.comports():
            self.listener.handle_new_port(port.device)
                
    def device_event(self, action, device):
        """Callback function for the device event.
        It calls the handle_new_port or handle_removed_port functions based on the action.
        """
        if action == 'add':
            self.listener.handle_new_port(device.device_node)
        elif action == 'remove':
            self.listener.handle_removed_port(device.device_node)