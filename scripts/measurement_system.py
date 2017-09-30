#!/usr/bin/env python

import rospy
from measurement_system.msg import measurement_msg
from vision.msg import VisionMessage


def estimator(data):
    alpha = 0.2
    estimate.x = alpha*estimate.x + (1-alpha)*data.x
    estimate.y = alpha*estimate.x + (1-alpha)*data.y
    estimate.th = data.th
    estimate.ball_x = data.ball_x
    estimate.ball_y = data.ball_y

    print data.x




def start():
    global estimate
    estimate = VisionMessage()

    rospy.init_node('measurement_system', anonymous=True)
    rate = rospy.Rate(10)

    pub = rospy.Publisher('measurement_system_topic', measurement_msg, queue_size = 10)
    rospy.Subscriber('pixel_to_metric_conversion_topic', VisionMessage, estimator)

    try:
       while not rospy.is_shutdown():
        pub.publish(estimate)
        rate.sleep()
    except rospy.ROSInterruptException:
        exit(1)




if __name__ == '__main__':
    try:
        start()
    except rospy.ROSInterruptException:
        pass
