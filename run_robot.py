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
from Xbox_value import XBOX_class
from IMU import read_imu_angle_N
from HardwareInterface import HardwareInterface

## TODO: run the robot endless, to test the waterproof performance

def main():
####################################################################################################
# Before you run the following command, you need to authorize to access the USB port -- /dev/ttyUSB0
# type in your terminal : sudo chmod 666 /dev/ttyUSB0 
##################yellow##################################################################################

    xbox = XBOX_class()
    xbox.initialize_xbox()
    # FIXME: need to reading the joystick data while controlling PWM
    # multi-threading
    xbox.get_xbox_status()
    print(xbox.done)

    N = 100
    Angle = read_imu_angle_N(N)
    print(Angle)
    print("IMU is working !")

    # create configuration of servo and thruster
    hardware_interface = HardwareInterface()
    print("PWM configuration of servos and thrusters are done!")
    
    print("servo will be working soon!")

    # TODO: thruster control with posture data (roll,pitch,yaw) euler angle from IMU feedback.
    # TODO: integrate into Wile(1) loop

    # Thruster control by PWM. 20210719
    pi = pigpio.pi()

    # pi.set_PWM_frequency(16,100)
    pi.set_PWM_frequency(12,100)

    # pi.set_servo_pulsewidth(16,1500)
    pi.set_servo_pulsewidth(12,1500)

    time.sleep(4)

    # pi.set_servo_pulsewidth(16,1450)
    pi.set_servo_pulsewidth(12,1560)

    # 

    # put two angle into servos, to test the waterproof performance of servos.s

    while True:

        joint_angles_1 = np.array ([[290,290,290,290],
                                    [290,290,290,290],
                                    [180,180,180,180]])
                                    # [180,180,180]])
        # joint_angles_2 = np.array([])
        hardware_interface.set_actuator_positions(joint_angles_1)
        time.sleep(1)
        joint_angles_2 = np.array ([[150,150,150,150],
                                    [150,150,150,150],
                                    [150,150,150,150]])

        hardware_interface.set_actuator_positions(joint_angles_2)
        time.sleep(1)


main()


