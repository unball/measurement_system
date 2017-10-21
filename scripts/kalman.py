#!/usr/bin/env python

import rospy
from measurement_system.msg import measurement_msg
from vision.msg import VisionMessage



def subscriber(data):
    kalman.x = data.x
    kalman.y = data.y
    kalman.th = data.th
    kalman.ball_x = data.ball_x
    kalman.ball_y = data.ball_y

    print data.x




def start():
    global kalman
    kalman = measurement_msg()

    rospy.init_node('measurement_system', anonymous=True)
    rate = rospy.Rate(10)

    pub = rospy.Publisher('measurement_system_topic', measurement_msg, queue_size = 10)
    rospy.Subscriber('pixel_to_metric_conversion_topic', VisionMessage, subscriber)

    try:
       while not rospy.is_shutdown():
        pub.publish(kalman)
        rate.sleep()
    except rospy.ROSInterruptException:
        exit(1)




if __name__ == '__main__':
    try:
        start()
    except rospy.ROSInterruptException:
        pass
