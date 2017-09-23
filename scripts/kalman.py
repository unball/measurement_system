#!/usr/bin/env python

import rospy
from measurement_system.msg import measurement_msg
from vision.msg import VisionMessage

def convert_msg(vision_msg): 
    measure_msg = measurement_msg()
    measure_msg.x = vision_msg.x
    measure_msg.y = vision_msg.y
    measure_msg.th = vision_msg.th
    measure_msg.ball_x = vision_msg.ball_x
    measure_msg.ball_y = vision_msg.ball_y
    return measure_msg

def main():
    global kalman
    kalman = VisionMessage()

    rospy.init_node('measurement_system', anonymous=True)
    rate = rospy.Rate(10)

    pub = rospy.Publisher('kalman_topic', VisionMessage, queue_size = 10)
    rospy.Subscriber('pixel_to_metric_conversion_topic', VisionMessage, subscriber)
    to_pub = convert_msg(kalman)
    try:
       while not rospy.is_shutdown():
        pub.publish(to_pub)
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
