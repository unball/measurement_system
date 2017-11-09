#!/usr/bin/env python

import rospy
from measurement_system.msg import measurement_msg
from vision.msg import VisionMessage
import planar
from math import fabs

class DisassemblyMessage(object):
    def __init__(self, message):
        self.x=list(message.x)
        self.y=list(message.y)
        self.th=list(message.th)
        self.ball_x=message.ball_x
        self.ball_y=message.ball_y



def estimator(data):
    local = DisassemblyMessage(data)
    for i in xrange(6):
        if not data.found[i] :
            local.x[i] = estimation.x[i]
            local.y[i] = estimation.y[i]
            local.th[i] = estimation.th[i]

    movingAvg(local)
    ballPredictor(local)
    estimation.ball_x_walls, estimation.ball_y_walls = wallsPrediction(local)
    # unityGain(local)
    

    prev_estimation.ball_x = estimation.ball_x
    prev_estimation.ball_y = estimation.ball_y


def wallsPrediction(data):
    speed_vector = planar.Vec2(estimation.ball_x_pred - data.ball_x,estimation.ball_y_pred - data.ball_y)
    speed_vector = planar.Vec2.normalized(speed_vector)
    ball_position = planar.Vec2(data.ball_x,data.ball_y)
    
    if (speed_vector.x != 0) and (speed_vector.y != 0):
        t_x_pos = (0.65 - ball_position.x)/speed_vector.x
        t_y_pos = (0.75 - ball_position.y)/speed_vector.y
        t_x_neg = (-0.65 - ball_position.x)/speed_vector.x
        t_y_neg = (-0.75 - ball_position.y)/speed_vector.y

        time_list = [(t_x_pos),(t_y_pos),(t_x_neg),(t_y_neg)]   
        time = min([i for i in time_list if i>0])

        walls_y = speed_vector.y * time + ball_position.y
        walls_x = speed_vector.x * time + ball_position.x

    elif speed_vector.x != 0:
        t_x_pos = (0.65 - ball_position.x)/speed_vector.x
        t_x_neg = (-0.65 - ball_position.x)/speed_vector.x

        time_list = [(t_x_pos),(t_x_neg)]   
        time = min([i for i in time_list if i>0])
        walls_y = ball_position.y
        walls_x = ball_position.x + speed_vector.y * time

    elif speed_vector.y != 0:
        t_y_pos = (0.75 - ball_position.x)/speed_vector.x
        t_y_neg = (-0.75 - ball_position.x)/speed_vector.x

        time_list = [(t_y_pos),(t_y_neg)]   
        time = min([i for i in time_list if i>0])
        walls_x = ball_position.x
        walls_y = ball_position.y + speed_vector.y * time
    else:
        walls_x = 0
        walls_y = 0

    return walls_x,walls_y       



def movingAvg(data):
    alpha = 0.4
    for i in range(3):
        estimation.x[i] = (alpha)*estimation.x[i] + (1-alpha)*data.x[i]
        estimation.y[i] = (alpha)*estimation.y[i] + (1-alpha)*data.y[i]
        estimation.th[i] = data.th[i]

    estimation.ball_x = (alpha)*estimation.ball_x + (1-alpha)*data.ball_x
    estimation.ball_y = (alpha)*estimation.ball_y + (1-alpha)*data.ball_y

vel_x = 0.0
vel_y = 0.0

def ballPredictor(data):
    global vel_x
    global vel_y
    beta = 0.1
    k = 1
    vel_x_data = estimation.ball_x - prev_estimation.ball_x
    vel_y_data = estimation.ball_y - prev_estimation.ball_y

    vel_x = (1-beta)*vel_x_data + (beta)*vel_x
    vel_y = (1-beta)*vel_y_data + (beta)*vel_y

    estimation.ball_x_pred = 0.1*(estimation.ball_x + vel_x*k) + 0.9*(data.ball_x)
    estimation.ball_y_pred = 0.1*(estimation.ball_y + vel_y*k) + 0.9*(data.ball_y)




def unityGain(data):
    estimation.x = data.x
    estimation.y = data.y
    estimation.th = data.th
    estimation.ball_x = data.ball_x
    estimation.ball_y = data.ball_y
    estimation.ball_x_pred = data.ball_x
    estimation.ball_y_pred = data.ball_y_pred


def start():
    global estimation, prev_estimation
    estimation = measurement_msg()
    prev_estimation = measurement_msg()


    rospy.init_node('measurement_system', anonymous=True)
    rate = rospy.Rate(30)

    pub = rospy.Publisher('measurement_system_topic', measurement_msg, queue_size = 1)
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
