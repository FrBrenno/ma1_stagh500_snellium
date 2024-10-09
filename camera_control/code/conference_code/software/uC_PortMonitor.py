import pyudev


class uC_PortMonitor:
    """Class to monitor the ports and detect the uC ports.
    It uses pyudev to monitor the ports and detect the uC ports changes.
    Thus, it notifies the listener about the changes.
    """

    def __init__(self, discoverer, baudrate):
        self.listener = discoverer
        self.baudrate = baudrate

        self.context = pyudev.Context()
        self.monitor = pyudev.Monitor.from_netlink(self.context)
        self.monitor.filter_by(subsystem="tty")
        self.observer = pyudev.MonitorObserver(self.monitor, self.device_event)

    def start(self):
        """Starts the monitoring of the p orts."""
        self.observer.start()
        print("Started monitoring ports...")

    def stop(self):
        """Stops the monitoring of the ports."""
        self.observer.stop()
        print("Stopped monitoring ports...")

    def scan_existing_ports(self):
        """Scans the existing ports to detect uC ports.
        It gets the list of ports and checks if they are uC ports.
        """
        print("Scanning existing ports...")
        for device in self.context.list_devices(subsystem="tty"):
            ## Filter the devices to get only the serial communication ports
            com_port_pattern = ["/dev/ttyS", "/dev/ttyUSB"]
            if any(pattern in device.device_node for pattern in com_port_pattern):
                ## DEBUG PURPOSES
                ## this port takes too much time
                if device.device_node == "/dev/ttyS0":
                    continue
                ## DEBUG PURPOSES
                self.device_event("add", device)

    def device_event(self, action, device):
        """Callback function for the device event.
        It calls the handle_new_port or handle_removed_port functions based on the action.
        """
        if action == "add":
            self.listener.handle_new_port(device.device_node)
        elif action == "remove":
            self.listener.handle_removed_port(device.device_node)
