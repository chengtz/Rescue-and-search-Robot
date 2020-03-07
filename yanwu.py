  GNU nano 2.5.3                                         File: publisher.py                                                                                         

#!/usr/bin/env python
# BEGIN ALL
# BEGIN SHEBANG
#!/usr/bin/env python
# END SHEBANG
 
# BEGIN IMPORT
import rospy
import RPi.GPIO as GPIO
import time
# END IMPORT
 
# BEGIN STD_MSGS
from std_msgs.msg import Int16
# END STD_MSGS
CHANNEL=36
GPIO.setmode(GPIO.BOARD)
GPIO.setup(CHANNEL,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) 
yanwu=GPIO.input(CHANNEL)
#GPIO.input(CHANNEL)
 
rospy.init_node('sense')
 
# BEGIN PUB
pub = rospy.Publisher('yanwu', Int16)
# END PUB
 
# BEGIN LOOP
rate = rospy.Rate(10)
 
#count = 0
while not rospy.is_shutdown():
    pub.publish(yanwu)
    rate.sleep()
# END LOOP
# END ALL

