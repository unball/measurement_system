#!/usr/bin/env python

import rospy
from measurement_system.msg import measurement_msg


def main():
    msg = measurement_msg
    pub = rospy.Publisher('measurement_system', measurement_msg, queue_size=10)
    rospy.init_node('measurement_node')
    rate = rospy.Rate(10)
    
    lista = [x for x in range(6)]
    try:
        while not rospy.is_shutdown():
            msg = measurement_msg()
            msg.x = lista
            msg.y = lista
            msg.th = lista
            msg.ball_x = 0
            msg.ball_y = 0

            pub.publish(msg)
            rate.sleep()

    except rospy.ROSInterruptException:
        exit(1)
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
