import RPi.GPIO as GPIO
import time

def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12,GPIO.IN)
    GPIO.setup(21,GPIO.OUT)
    pass

def beep():
    while GPIO.input(12):
        GPIO.output(21,GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(21,GPIO.HIGH)
        time.sleep(0.5)
def detct():
    for i in range(1,101):
        if GPIO.input(12) == True:
            print "JIT rescue robot:  Find somebody !"
            beep()
        else:
            GPIO.output(21,GPIO.HIGH)
            print "JIT rescue robot finding ..."
        time.sleep(2)

time.sleep(5)
init()
detct()
GPIO.cleanup()
