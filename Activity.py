from GPIO import SensorManager
from Socket import Server

class Activity :
	""" This class is the mother class for all activities """

	
	def gpioUpdate(self, value, pinName) :
		""" Called when a sensor in sensors list has changed
			value : new sensor value. O or 1 for digital. O to 100 for analog.
			pinName : pin name as write in Pin.py class
		"""
		pass

	def serverUpdate(self, tab) :
		""" Called when server receved message 
			tab : tab wiht [function, opti1, ..., value, ...]
		"""
		pass
	
	def setupSensors(self) :
		""" setup sensors wiht the same methode call back gpioUpdate()
		    sensors list will be created in daughter class
		"""
		for sensor in self.sensors :
			self.manager.addListener(sensor, self.gpioUpdate)

	def __init__(self, listingServer) :
		""" Setup SensorManger and listing sensors.
			Setup Server and listing if listingServer is True
		"""
		# Setup sensor listing
		self.manager = SensorManager()
		self.setupSensors()
		#Setup server listing
		self.server = Server(2014)
		if listingServer :
			self.server.addListener(self.serverUpdate)
		print "Activity instancied"

	def stop(self) :
		pass
