'''
Filename: /home/guoyucan/ServoDogVersion1.0/run_robot.py
Path: /home/guoyucan/ServoDogVersion1.0
Created Date: Thursday, July 15th 2021, 3:04:34 pm
Author: guoyucan

Copyright (c) 2021 Your Company
'''
import time 
import numpy as np 
import os
import pigpio

from IMU import read_imu_angle_N
from HardwareInterface import HardwareInterface

## TODO: run the robot endless, to test the waterproof performance

def main():
####################################################################################################
# Before you run the following command, you need to authorize to access the USB port -- /dev/ttyUSB0
# type in your terminal : sudo chmod 666 /dev/ttyUSB0 
####################################################################################################


    N = 100
    Angle = read_imu_angle_N(N)
    print(Angle)
    print("IMU is working !")

    # create configuration of servo and thruster
    hardware_interface = HardwareInterface()
    print("PWM configuration of servos and thrusters are done!")
    
    print("servo will be working soon!")

    while True:

        joint_angles_1 = np.array ([[200,200,200,200],
                                    [200,200,200,200],
                                    [180,180,180,180]])
                                    # [180,180,180]])
        # joint_angles_2 = np.array([])
        hardware_interface.set_actuator_positions(joint_angles_1)
        time.sleep(3)
        joint_angles_2 = np.array ([[150,150,150,150],
                                    [150,150,150,150],
                                    [150,150,150,150]])

        hardware_interface.set_actuator_positions(joint_angles_2)
        time.sleep(3)





main()
