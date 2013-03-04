import usb.core
import usb.util
import config

from PySide.QtCore import *
from PySide.QtGui import *

from UsbDevice import UsbDevice

class Device(UsbDevice):

	def __init__(self):
		
		UsbDevice.__init__(self, config.device_id[0], config.device_id[1])
		
		self.interface =    config.device_ep["interface"]
		self.out_endpoint = config.device_ep["out"]
		self.in_endpoint =  config.device_ep["in"]
		
		
	def enterBootloader(self):
		try:
			self.write(config.enter_bootloader_command)
		except:
			pass
