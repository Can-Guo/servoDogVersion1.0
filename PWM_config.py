#####################################################################
#   The first servo test of the servo_dog Version 1.0
#   Date : 2021.07.12
#   Name : guoyucan, 12032421@mail.sustech.edu.cn
#   Function : Test the PWM generation of the Raspberry 4B
#              and the hareware connection of 14 servos
#              and 2 thrusters.
#    
#####################################################################



import numpy as np 
import math
import time
import os
import pigpio

class Servo_PWM_Parameter:
    def __init__(self):
        self.neutral_position = 1500  # after zero calibration, us
        self.range = 2500  # us
        self.pins = np.array([[2, 14, 18, 23], [3, 15, 27, 24], [4, 17, 22, 25]])  # the pins used for 12 servos of legs
        self.freq = 100 # the frequency of the PWM output to servos

    def initial_servo_PWM(self):

        return

    def loop_servo_PWM(self):

        return

class Thruster_PWM_Para:
    def __int__(self):
        self.neutral_position = 1500  # us
        # self.smallest_position = 1100 # us
        # self.biggest_position = 1900 # us
        # self.MAX_PWM_derivation = 500 # us
        # self.dead_zone = 50 # us
        self.range = 2000
        self.pin = np.array([])
        self.freq = 50 # 50Hz for T200 Thruster by Bluerobotics.com

    def intial_thruster_PWM(self):
        return

    def loop_thruster_PWM(self):
        return
    
