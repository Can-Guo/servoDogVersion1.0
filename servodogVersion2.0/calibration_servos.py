'''
Date: 2021-11-17 15:01:59
LastEditors: Guo Yuqin,12032421@mail.sustech.edu.cn
LastEditTime: 2021-11-17 16:20:11
FilePath: /servoDogVersion1.0/servodogVersion2.0/calibration_servos.py
'''
'''
*********************************************************************************************
  *File: calibration_servos.py
  *Project: servodogVersion2.0
  *Filepath: /home/guoyucan/ServoDogVersion1.0/servodogVersion2.0/calibration_servos.py 
  *File Created: Wednesday, 17th November 2021 2:38:35 pm
  *Author: Guo Yucan, 12032421@mail.sustech.edu.cn 
  *Last Modified: Wednesday, 17th November 2021 2:38:39 pm
  *Modified By: Guo Yucan, 12032421@mail.sustech.edu.cn 
  *Copyright @ 2021 , BionicDL LAB, SUSTECH, Shenzhen, China 
*********************************************************************************************
'''

import pigpio 
import numpy as np 
import time 

def main(pin):
    pi = pigpio.pi()
    pi.set_PWM_frequency(pin,50)
    pi.set_PWM_range(pin,2500)

    # while True:

    pi.set_servo_pulsewidth(pin,1000)
    time.sleep(2)
    pi.set_servo_pulsewidth(pin,1500)
    time.sleep(2)
    pi.set_servo_pulsewidth(pin,2000)
    time.sleep(2)


    pi.set_servo_pulsewidth(pin,1500)
    time.sleep(2)

    # pi.set_servo_pulsewidth(pin,2000)
    # time.sleep(2)
    # pi.set_servo_pulsewidth(pin,1500)
    # time.sleep(2)
    # pi.set_servo_pulsewidth(pin,1000)
    # time.sleep(2)

main(2)
        
