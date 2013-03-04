#!/usr/bin/gksudo /usr/bin/python
import sys
sys.stderr = sys.stdout

from PySide.QtUiTools import QUiLoader

from PySide.QtCore import *
from PySide.QtGui import *
import PySide.QtXml
import usb.core
import os

from lib import *
		

class Manager(QObject):
	def __init__(self):
		QObject.__init__(self)
		
		self.boot = BootDevice()
		self.dev = Device()
		
		self.dev.onOpened.connect(self.on_device_opened)
		self.boot.onOpened.connect(self.on_boot_opened)
		
		self.fw = None
		
		
	def on_start_app(self):
		self.boot.bootApplication()
		
	def on_main_button_pressed(self):
		print self.dev.opened, self.boot.opened
		if self.dev.opened:
		
			self.dev.enterBootloader()
			self.parent().interface.mainButton.setEnabled(False)
			
		#begin flashing	
		elif self.boot.opened:
		
			def progress_cb(percent):
				self.parent().interface.progressBar.setValue(percent)
				if percent == 100:
					self.boot.bootApplication()
					
			f = self.parent().interface.fwFile.text()
			if f != "":
					self.fw = Firmware(f)
		
			self.boot.writeFirmware(self.fw, progress_cb)
			self.parent().interface.mainButton.setEnabled(False)
			self.parent().interface.startApp.setEnabled(False)
			
	def on_firmware_selected(self):
		f = self.parent().interface.fwFile.text()
		if f != "":
			try:
			
				self.fw = Firmware(f)
			
			except:
			
				self.parent().interface.setText("")
			
			else:
				#TODO: check ascii chars
				self.parent().interface.fileFwVer.setText(self.fw.getVersion())
			
		
	def on_device_opened(self, connected):
		print "on_device_opened", connected

		self.parent().interface.versionStr.setText("Waiting for bootloader...")
		self.parent().interface.versionStr.setEnabled(False)
		self.parent().interface.mainButton.setText("Enter Bootloader")	
		self.parent().interface.startApp.setEnabled(False)
		
		if connected:
			self.parent().interface.mainButton.setProperty("enabled", True)
			self.parent().interface.statusStr.setText("<font color='green'>Connected</font>")
			
		elif not connected and not self.boot.opened:
			self.parent().interface.mainButton.setProperty("enabled", False)
			self.parent().interface.statusStr.setText("<font color='red'>Disconnected</font>")			
		
	def on_boot_opened(self, connected):
		if connected:
			self.parent().interface.mainButton.setProperty("enabled", True)
			self.parent().interface.statusStr.setText("<font color='green'>Bootloader</font>")
			self.parent().interface.versionStr.setEnabled(True)
			self.parent().interface.startApp.setEnabled(True)
			
			version = self.boot.getVersion()
			
			self.parent().interface.versionStr.setText(version)
			self.parent().interface.mainButton.setText("Flash")	
			self.parent().interface.mainButton.setEnabled(True)	
			
		elif not connected and not self.dev.opened:
			self.parent().interface.mainButton.setProperty("enabled", False)
			self.parent().interface.statusStr.setText("<font color='red'>Disconnected</font>")	
			self.parent().interface.versionStr.setEnabled(False)
			self.parent().interface.mainButton.setText("Enter Bootloader")	
			self.parent().interface.startApp.setEnabled(False)
	
	def check(self):
	
		if self.boot.isAttached() and not self.boot.opened:
			try:
				self.boot.open()
			except usb.core.USBError, e:
				dialog = QMessageBox.warning(None, "Opening device failed", str(e))
				exit(0)
			
		elif self.dev.isAttached() and not self.dev.opened:
			try:
				self.dev.open()
			except usb.core.USBError, e:
				dialog = QMessageBox.warning(None, "Opening device failed", str(e))
				exit(0)
					
		
	def start(self):
		self.parent().interface.mainButton.clicked.connect(self.on_main_button_pressed)
		self.parent().interface.fwFile.textChanged.connect(self.on_firmware_selected)
		self.parent().interface.startApp.clicked.connect(self.on_start_app)
		self.check()
		self.startTimer(500)
		
	def timerEvent(self, event):
		self.check()



class Main(QApplication):

	def __init__(self):
		QApplication.__init__(self, sys.argv)
				
		loader = QUiLoader()
		
		self.settings = QSettings("walmis", "FirmwareFlashTool")	
		
		buf = QBuffer()
		buf.setData(GuiDesc.GuiDesc)
		
		self.interface = loader.load(buf)
		self.interface.setFixedSize(self.interface.width(), self.interface.height())
		
		self.mainButton = self.interface.mainButton
		
		
		
		def fileDialog():
			if self.interface.fwFile.text() != "":
				d = os.path.dirname(self.interface.fwFile.text())
			else:
				d = ""
			
			f = QFileDialog.getOpenFileName(self.interface, "Select Firmware Image", dir=d, filter="Firmware images (*.fw)")[0]
			
			
			
			if f != "":
				self.interface.fwFile.setText("")
				self.interface.fwFile.setText(f)
				self.settings.setValue("last_file", f)
				self.settings.sync()
		
		self.interface.browseBtn.clicked.connect(fileDialog)
		
		self.manager = Manager()
		self.manager.setParent(self)
		
		self.manager.start()

		self.interface.fwFile.setText(self.settings.value("last_file", ""))
		
		
		
		self.interface.show()

try:		
	app = Main()
	app.exec_()
except Exception, e:
	dialog = QMessageBox.critical(None, "Error", str(e))
	
