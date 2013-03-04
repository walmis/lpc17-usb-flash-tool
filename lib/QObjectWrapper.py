from PySide.QtCore import *
from PySide.QtGui import *


class QObjectWrapper(QObject):
	_properties = {}
  
	def __init__(self, **kwargs):
		QObject.__init__(self)
		print dir(self.__class__.__dict__)
		print self.__class__._properties
		

		for key, val in self._properties.iteritems():
		    self.__dict__['_'+key] = kwargs.get(key, val())
		    
		print self.__dict__
		
		for key, value in self._properties.iteritems():
			nfy = self.__dict__['_nfy_'+key] = Signal()

			def _get(key):
				 def f(self):
					  return self.__dict__['_'+key]
				 return f

			def _set(key):
				 def f(self, value):
					  self.__dict__['_'+key] = value
					  self.__dict__['_nfy_'+key].emit()
				 return f

			set = self.__dict__['_set_'+key] = _set(key)
			get = self.__dict__['_get_'+key] = _get(key)

			self.__dict__[key] = Property(value, get, set, notify=nfy)
			
		print dir(self)

	def __repr__(self):
		values = ('%s=%r' % (key, self.__dict__['_'+key]) \
				  for key, value in self._properties.iteritems())
		return '<%s (%s)>' % (self.__class__.__name__, ', '.join(values))


