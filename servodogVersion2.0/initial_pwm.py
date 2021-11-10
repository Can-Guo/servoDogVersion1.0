'''
Date: 2021-11-10 22:17:22
LastEditors: Guo Yuqin,12032421@mail.sustech.edu.cn
LastEditTime: 2021-11-11 01:57:09
FilePath: /servodogVersion2.0/initial_pwm.py
'''

import numpy as np 

POWER = np.array([0.25, 0.50, 0.75, 1.00])  ## Power scaler to control the Power of T200 Thruster

class Leg_PWM_Parameter:
    def __init__(self):
        self.leg_neutral_position = 1500 
        self.leg_range = 2500
        self.leg_pins = np.array([[2,14,18,23],[3,15,27,24],[4,17,22,25]])
        self.leg_frequency = 100
    
    

class USRL_PWM_Parameter:
    def __init__(self):
        self.T200_neutral_position = 1500
        self.T200_range = 2000
        self.T200_pins = np.array([12,16])  # T200 -> 12,16 PIN
        self.T200_frequency = 50
        self.T200_power_scale = POWER[0]

        self.servo_neutral_position = 1500
        self.servo_range = 2500
        self.servo_pins = np.array([20,21]) # servo -> 20,21 PIN
        self.servo_frequency = 100

        


