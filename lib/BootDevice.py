import usb.core
import usb.util
import config
import struct

from PySide.QtCore import *
from PySide.QtGui import *

from UsbDevice import UsbDevice

class BootDevice(UsbDevice):

	def __init__(self):
		
		UsbDevice.__init__(self, config.boot_id[0], config.boot_id[1])
		
		self.interface =    config.boot_ep["interface"]
		self.out_endpoint = config.boot_ep["out"]
		self.in_endpoint =  config.boot_ep["in"]

	def bootApplication(self):
		try:
			self.write(":BOOT\n")
		except:
			pass
			
	def getVersion(self):
		self.write(":GETVERSION\n")
		return self.read(20)
		
	def writeFirmware(self, firmware, progress_cb=None):
		print "Write firmware"
		self.write(":FLASH\n" + struct.pack("L", firmware.getSize()))
		
		data = firmware.getData()
		
		offset = [0]
		
		timer = QTimer()
		
		
		def write():
			self.write(data[offset[0]:offset[0]+512])
			offset[0] += 512
			
			if progress_cb:
				progress_cb( int(offset[0] / firmware.getSize() * 100) ) 
			
			if offset[0] >= firmware.getSize():
				timer.stop()
				print self.read(200)
				
		timer.timeout.connect(write)
		timer.start()	
			
			#progress.setValue()
			
