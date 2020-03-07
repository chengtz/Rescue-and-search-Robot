#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
# BEGIN IMPORT
import rospy
import RPi.GPIO as GPIO
import time
# END IMPORT
 
# BEGIN STD_MSGS
from std_msgs.msg import String
# END STD_MSGS
CHANNEL=36
GPIO.setmode(GPIO.BOARD)
GPIO.setup(CHANNEL,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

#GPIO.input(CHANNEL)

rospy.init_node('sense')

# BEGIN PUB
pub = rospy.Publisher('yanwu', String)
# END PUB
 
# BEGIN LOOP
rate = rospy.Rate(1)

#count = 0


try:
         while True:
          status=GPIO.input(CHANNEL)
          if status == True:
                        print ( ' 正常 ' )
                        yanwu = '当前有害气体正常'
                        pub.publish(yanwu)
          else:
                        print ( '检测到有害气体！！！' )
                        yanwu = '检测到有害气体！！！'
                        pub.publish(yanwu)
          time.sleep(1)
except KeyboardInterrupt:
            GPIO.cleanup()
