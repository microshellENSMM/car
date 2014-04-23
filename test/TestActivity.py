from Activity import Activity
from GPIO import Output, PWM
from Pin import Pin
from Commands import Commands
import time

class BlinkActivity (Activity) :

    def __init__(self) :
        self.state = False
        self.led = Output(Pin.led)
        self.sensors = [Pin.bouton]
        Activity.__init__(self, True)

    def gpioUpdate(self, value, pinName) :
        if pinName == Pin.bouton and value ==1 :
            self.switchLED()


    def serverUpdate(self, tab) :
        if tab[0] == Commands.light :
            self.switchLED()

    def switchLED(self) :
        self.state = not self.state
        if self.state :
            self.led.high()
        else :
            self.led.low()

    def stop(self) :
        Activity.stop(self)

blink = BlinkActivity()
time.sleep(10)
blink.stop()
