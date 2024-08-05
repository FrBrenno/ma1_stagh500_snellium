import pytest
import serial

from unittest.mock import patch, Mock

from uC_Monitor import uC_Monitor


class TestMonitor:
    def setup_method(self):
        self.monitor = uC_Monitor()
        self.monitor.observer = Mock()
        self.monitor.is_uC_port = Mock()
        
    @patch('serial.tools.list_ports.comports')
    def test_scan_existing_ports(self, mock_comports):
        mock_port_1 = serial.tools.list_ports_common.ListPortInfo('/dev/ttyUSB0')
        mock_port_2 = serial.tools.list_ports_common.ListPortInfo('/dev/ttyUSB1')
        mock_port_3 = serial.tools.list_ports_common.ListPortInfo('/dev/ttyUSB2')
        mock_comports.return_value = [mock_port_1, mock_port_2, mock_port_3]
        
        self.monitor.is_uC_port.side_effect = [True, False, True]
        
        self.monitor.scan_existing_ports()
        
        assert len(self.monitor.uC_port_set) == 2
        assert '/dev/ttyUSB0' in self.monitor.uC_port_set
        assert '/dev/ttyUSB2' in self.monitor.uC_port_set
        assert '/dev/ttyUSB1' not in self.monitor.uC_port_set
     
    @patch('serial.tools.list_ports.comports')
    def test_device_event_add(self, mock_comports):
        mock_port = serial.tools.list_ports_common.ListPortInfo('/dev/ttyUSB0')
        mock_port.device = '/dev/ttyUSB0'
        mock_comports.return_value = [mock_port]
        
        self.monitor.is_uC_port.return_value = True
        
        self.monitor.device_event('add', mock_port)
        
        assert len(self.monitor.uC_port_set) == 1
        assert '/dev/ttyUSB0' in self.monitor.uC_port_set
    