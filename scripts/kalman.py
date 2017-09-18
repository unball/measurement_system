#!/usr/bin/env python

import rospy
from measurement_system.msg import measurement_msg
from vision.msg import VisionMessage

def main():
    global kalman
    kalman = VisionMessage()

    rospy.init_node('measurement_system', anonymous=True)
    rate = rospy.Rate(10)

    pub = rospy.Publisher('kalman_topic', VisionMessage, queue_size = 10)
    rospy.Subscriber('pixel_to_metric_conversion_topic', VisionMessage, subscriber)

    try:
       while not rospy.is_shutdown():
        pub.publish(kalman)
        rate.sleep()
    except rospy.ROSInterruptException:
        exit(1)



def subscriber(data):
    kalman = data


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
