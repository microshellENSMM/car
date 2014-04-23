from GPIO import *
from Pin import Pin

def boutonPressed(value, pinSensor) :
	print "Etat du bouton {}".format(value)

def potoMoved(value, pinSensor) :
	print "Etat du poto {}".format(value)
	if value is 0 :
		managerA.stop()
		managerB.stop()
		print "Manager stop"

manager = SensorManager()
manager.addListener(Pin.bouton, boutonPressed)
manager.addListener(Pin.poto, potoMoved)



