#!/usr/bin/env python

import rospy
from measurement_system.msg import measurement_msg
from vision.msg import VisionMessage



def estimator(data):
    #movingAvg(data)
    unityGain(data)



def movingAvg(data):
    alpha = 0.3
    for i in xrange(0,2):
        estimation.x[i] = (alpha)*estimation.x[i] + (1-alpha)*data.x[i]
        estimation.y[i] = (alpha)*estimation.y[i] + (1-alpha)*data.y[i]
        estimation.th[i] = (alpha)*estimation.th[i] + (1-alpha)*data.th[i]
        pass

    estimation.ball_x = (alpha)*estimation.ball_x + (1-alpha)*data.ball_x
    estimation.ball_y = (alpha)*estimation.ball_y + (1-alpha)*data.ball_y

    pass


def unityGain(data):
    estimation.x = data.x
    estimation.y = data.y
    estimation.th = data.th
    estimation.ball_x = data.ball_x
    estimation.ball_y = data.ball_y


def start():
    global estimation
    estimation = VisionMessage()

    rospy.init_node('measurement_system', anonymous=True)
    rate = rospy.Rate(10)

    pub = rospy.Publisher('measurement_system_topic', measurement_msg, queue_size = 10)
    rospy.Subscriber('pixel_to_metric_conversion_topic', VisionMessage, estimator)

    try:
       while not rospy.is_shutdown():
        pub.publish(estimation)
        rate.sleep()
    except rospy.ROSInterruptException:
        exit(1)




if __name__ == '__main__':
    try:
        start()
    except rospy.ROSInterruptException:
        pass