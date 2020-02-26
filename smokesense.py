import RPi.GPIO as GPIO
import time

CHANNEL=36
GPIO.setmode(GPIO.BOARD)
GPIO.setup(CHANNEL,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)


try:
         while True:
          status=GPIO.input(CHANNEL)
          #print(status)
          if status == True:
                        print ('OK')
          else:
                        print ('DANGER')
          time.sleep(0.1)
except KeyboardInterrupt:
            GPIO.cleanup()
