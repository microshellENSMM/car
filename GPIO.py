import Adafruit_BBIO.GPIO as gpio
import Adafruit_BBIO.PWM as pwm
import Adafruit_BBIO.ADC as adc

from Pin import Pin
import threading
import time

class Output :
    """ class implentes the Adafruit_BBIO to use digital output pin"""

    def __init__(self, pin) :
        """ initialize the gpio by is name like P9_11"""
        self.pin = pin
        gpio.setup(self.pin, gpio.OUT)

    def high(self) :
        """ set the gpio to high"""
        gpio.output(self.pin, gpio.HIGH)

    def low(self) :
        gpio.output(self.pin, gpio.LOW)

    def remove(self) :
        """ remove the gpio status"""
        gpio.cleanup()


class Input : 
    """class implementes the Adafruit_BBIO to use digital input pin"""

    def __init__(self, pin):
        """initialize the gpio by is name like P9_11"""
        self.pin = pin
        gpio.setup(pin, gpio.IN)

    def getValue(self) :
        """ return the pin value True for high False for low"""
        if gpio.input(self.pin) :
            return 1
        else :
            return 0

    def getPin(self) :
        return self.pin

class PWM : 
    """class implementes the Adafruit_BBIO to use pwm output pin"""

    def __init__(self, pin, freq=2000, polarity=0) :
        """ initialize the pwm gpio by is name like P9_11
        frequence is set by default at 2000, polarity at 0"""
        self.pin = pin
        pwm.start(pin,0)

    def dutyCycle(self, value) :
        """ set the duty cycle value, which goest from 0 to 100"""
        value = min(value, 100)
        value = max(value, 0)
        pwm.set_duty_cycle(self.pin, value)

    def remove(self) :
        """ remove the pin"""
        pwm.stop(self.pin)
        pwm.cleanup()

class Analog : 
    """class implentes the Adafruit_BBIO to use ADC pin"""
    
    def __init__(self, pin):
        self.pin = pin
        adc.setup()
        print "VOLTAGE ABOVE 1.8V IS FORBIDDEN"
        print "AUCUN VOLTAGE AU DESSUS DE 1.8 EST AUTORISE"

    def getValue(self):
        """return the analog value which goes from 0 to 100 """
        # all nulber after 0.01 are deleted
        return int(adc.read(self.pin)*100)

    def getVoltage(self):
        """return the voltage wich goes from 0 to 1.8"""
        return getValue()*1.8

    def getPin(self) :
        return self.pin

class Sensor :
    """ This class represent a sensor digital or analog pin.
        If during a update() call, the sensor value has changed, all listener attached through a Observer pattern are updated.
        You can't use it directly, but you can instance it by SensorManager.addListenerAtSensor(pinSensor, listener)
    """

    def __init__(self, inputObject) :
        self.inputObject = inputObject
        self.previousValue = inputObject.getValue()
        self.listeners = []

    def getPreviousValue(self) :
        """ return the previous value recorded by the sensor"""
        return self.previousValue

    def isChanged(self, value) :
        """ return True if the value returned by the sensor has been changed, False else """
        if value is not self.previousValue :
            self.previousValue = value
            return True
        else :
            return False

    def updateListeners(self, value) :
        """ updtae all listeners attached with the new value
            Each listener is called in a new thread"""
        for listener in self.listeners :
            thread = threading.Thread(None, listener, None, (value, self.inputObject.getPin(), ), {} )
            thread.start()

    def update(self) :
        """ ckeck if value has changed by isChangde then call updateListener"""
        value = self.inputObject.getValue()
        if self.isChanged(value) :
            self.updateListeners(value)

    def addListener(self, listener) :
        """ Add listener to update"""
        self.listeners.append(listener)

    def removeListener(self, listener) :
        """ remove listener from update"""
        if listener in self.listeners :
            self.listeners.remove(listener)

    
    
class SensorManager :
    """ This class setup all pin input digital or analog belong to Pin class.
        You can catch any changed sensor value by adding a listener (function) for the selected pin.
        This object is a singleton.
    """
    
    class __impl :
        """ This class is the 'True' SensorManager wrapped in the above class to be a Singleton"""

        def __init__(self) :
            """ Set up all Sensor returned by Pin.getSensors() """
            self.sensors = {}
            pins = Pin.getSensors()
            for pin in pins :
                # We check if it's an analog sensor
                if int(pin[3:5]) in range(33, 41) :
                    self.sensors[pin] = Sensor(Analog(pin))
                
                # Else it's a digital sensor
                else :
                    self.sensors[pin] = Sensor(Input(pin))

            thread = threading.Thread(None, self.loop, None, (), {})
            thread.start()
            self.resume = True
            print self.sensors
            print "Manager is set up"

        def loop(self) :
            """This is the endless while, which check all sensor states changes"""
            while(self.resume) :
                for sensor in self.sensors.values() :
                    sensor.update()
                time.sleep(0.01)


        def id(self) :
            """ Return the instance id. Useful to debug the singleton patern"""
            return id(self)
        
        def addListener(self, pinName, function) :
            """ Add a listener on a pinName"""
            self.sensors[pinName].addListener(function)
            print "listener added"

        def stop(self) :
            """ set resume at False to stop loop"""
            self.resume = False

    __instance = None

    def __init__(self) :


        if SensorManager.__instance is None :
            SensorManager.__instance = SensorManager.__impl()

        self.__dict__["_SensorManager__instance"] = SensorManager.__instance

    def __getattr__(self, attr) :
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value) :
        return setattr(self.__instance, attr, value)

