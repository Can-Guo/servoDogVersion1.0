'''
Date: 2021-11-17 15:01:59
LastEditors: Guo Yuqin,12032421@mail.sustech.edu.cn
LastEditTime: 2021-11-17 22:47:04
FilePath: /servodogVersion2.0/initial_robot.py
'''
'''
*********************************************************************************************
  *File: initial_robot.py
  *Project: servodogVersion2.0
  *Filepath: /home/guoyucan/ServoDogVersion1.0/servodogVersion2.0/initial_robot.py 
  *File Created: Wednesday, 17th November 2021 10:54:46 am
  *Author: Guo Yucan, 12032421@mail.sustech.edu.cn 
  *Last Modified: Wednesday, 17th November 2021 10:54:51 am
  *Modified By: Guo Yucan, 12032421@mail.sustech.edu.cn 
  *Copyright @ 2021 , BionicDL LAB, SUSTECH, Shenzhen, China 
*********************************************************************************************
'''

import pigpio
import numpy as np 
from Hardware_Config import Hardware_Class


class Initial_Robot:
    def __init__(self):
        self.hardware_class = Hardware_Class()
        
    
    def initial_robot(self):
        self.hardware_class.initialize_leg_pwm()
        self.hardware_class.initialize_usrl_pwm()
    
    
    