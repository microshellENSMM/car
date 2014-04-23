from GPIO import *
import time

pin = "P9_13"
# Ouput Test
print "******Debut test output******"
led = Output(pin)
led.high()
time.sleep(3)
led.low()
print "******fin test output******"
time.sleep(2)

# PWM Test
def loop():
	
	for i in range(0, 100, 1) :
		pwm.dutyCycle(i)
		time.sleep(0.020)
	for i in range(100, -1, -1) :
		pwm.dutyCycle(i)
		time.sleep(0.020)

print "******Debut test pwm******"
pin = "P9_14"
pwm = PWM(pin)
loop()
print "fin test pwm"

print "debut test input"
print "APPUYER SUR LE BOUTON"
bouton = Input("P9_12")
while  bouton.getValue() == False :
	led.high()
led.low()
loop()
print "******fin test input******"

print "******Debut test Analog******"
print "FAIRE TOURNER LE POTO"
poto = Analog("P9_36")
while poto.getValue() > 0 :
	pwm.dutyCycle(poto.getValue())

print "******Fin test Analog******"
