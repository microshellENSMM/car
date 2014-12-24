from Activity import Activity
from GPIO import Output, PWM
from Pin import Pin
from Commands import Commands
import time

class LightActivity (Activity) :

    def __init__(self) :
        self.ledFrein = Output(Pin.led)

    
        self.sensors = [Pin.pedaleFrein]
        Activity.__init__(self, False)

    def gpioUpdate(self, value, pinName) :
        if pinName is Pin.pedaleFrein :
            if value >= 10 :
                self.ledFrein.high()
            else :
                self.ledFrein.low()
    def serverUpdate(self, tab) :
        pass


    def stop(self) :
        pass

