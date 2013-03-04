from PySide.QtCore import *
from PySide.QtGui import *
import os

class Firmware(QObject):

	def __init__(self, filename):
		QObject.__init__(self)
		print "Loading", filename
		
		self.file = open(filename, "rb")
		self.size = os.path.getsize(filename) - 16
		
		self.version = self.file.read(16)
		
		if self.size % 512 != 0:
			raise Exception("Invalid firmware file")
			
			
		self.data = self.file.read()
	
	
	def getVersion(self):
		return self.version
	
	def getData(self):
		return self.data
		
	def getSize(self):
		return len(self.data)
