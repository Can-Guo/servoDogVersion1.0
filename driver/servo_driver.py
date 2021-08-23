'''
Filename: /home/guoyucan/ServoDogVersion1.0/driver/servo_driver.py
Path: /home/guoyucan/ServoDogVersion1.0/driver
Created Date: Monday, August 23rd 2021, 10:44:17 am
Author: guoyucan

Copyright (c) 2021 SUSTECH
'''

from source.HardwareInterface import joint_deg_to_pulse_width
import numpy as np
from numpy.lib.function_base import select 
import pigpio  # the module to configurate the hardware, for Raspberrypi
               # For other hardware, please find another module to do the job.

class Servo_PWM:
    def __init__(self):
        # 
        print("Initializing the servo!")

        self.neutral_position = 1500  # after zero calibration, us
        self.range = 2500             # us
        self.pin = np.array([2])     # the pins used for the servo you use for the end effector.
        self.freq = 100               # the frequency of the PWM output for selected servos
        
        # initialize pwm for raspberrypi
        self.pi = pigpio.pi()
        self.pi.set_PWM_frequency(self.pin, self.freq)
        self.pi.set_PWM_range(self.pin, self.range)

        print("Initialization done.")

    def servo_calibration(self,initial_angle=0):

        print("Calibration begins...")
        self.send_deg_to_servo(initial_angle)
        print("Calibration Result: ")
        
        return

    def joint_deg_to_pulse_width(self,joint_angle=180): 
        # according to the mannual of servo motor by XUNLONGZHE.com
        # url : https://item.taobao.com/item.htm?spm=a1z10.5-c-s.w4002-17909957398.71.cd013fdd6F6uHw&id=616071138320

        pulse_width = 2000 * joint_angle / 360.0 + 500
        
        return (int)(pulse_width)

    def send_deg_to_servo(self,joint_angle):

        self.pi.set_servo_pulsewidth(self.pin,joint_deg_to_pulse_width(joint_angle))

        print("Pin : %d | Angle : %d", (self.pin, joint_angle))

        return 

