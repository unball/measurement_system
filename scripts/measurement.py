#!/usr/bin/env python

import rospy
from measurement_system.msg import measurement_msg
from vision.msg import VisionMessage

class DisasseblyMessage(object):
    def __init__(self, message):
        self.x=list(message.x)        
        self.y=list(message.y)        
        self.th=list(message.th)
        self.ball_x=message.ball_x
        self.ball_y=message.ball_y      



def estimator(data):
    local=DisasseblyMessage(data)
    for i in xrange(6):
        if not data.found[i] :
            local.x[i]=estimation.x[i]
            local.y[i]=estimation.y[i]
            local.th[i]=estimation.th[i]
    
    movingAvg(local)
    #unityGain(local)



def movingAvg(data):
    alpha = 0.4
    for i in range(3):
        estimation.x[i] = (alpha)*estimation.x[i] + (1-alpha)*data.x[i]
        estimation.y[i] = (alpha)*estimation.y[i] + (1-alpha)*data.y[i]
        estimation.th[i] = data.th[i]

    
    estimation.ball_x = (alpha)*estimation.ball_x + (1-alpha)*data.ball_x
    estimation.ball_y = (alpha)*estimation.ball_y + (1-alpha)*data.ball_y



def unityGain(data):
    estimation.x = data.x
    estimation.y = data.y
    estimation.th = data.th
    estimation.ball_x = data.ball_x
    estimation.ball_y = data.ball_y


def start():
    global estimation
    estimation = measurement_msg()

    rospy.init_node('measurement_system', anonymous=True)
    rate = rospy.Rate(30)

    pub = rospy.Publisher('measurement_system_topic', measurement_msg, queue_size = 10)
    rospy.Subscriber('pixel_to_metric_conversion_topic', VisionMessage, estimator)
    print('Measurement node started')
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
        exit(1)
