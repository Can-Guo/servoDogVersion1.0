'''
Date: 2021-11-10 23:18:34
LastEditors: Guo Yuqin,12032421@mail.sustech.edu.cn
LastEditTime: 2021-11-10 23:20:25
FilePath: /servoDogVersion1.0/servodogVersion2.0/Kinematics.py
'''
## TODO:  Kinematics(forward and inverse) for USRL robot
## Data: 20211110 - 20211117

import matplotlib.pyplot as plt
from mpmath.functions.functions import re
import numpy as np 
import math
import bezier
import sympy

class Kinematics_class():

    def __init__(self):
        pass 


    def bezier_generate(nodes=np.asfortranarray([[0.0, 122.5/np.sqrt(2), 245/np.sqrt(2)],[0.0, 122.5/np.sqrt(2), 0]]),degree=2):
        ### default nodes: 
        # nodes1 = np.asfortranarray([
        #     [0.0, 122.5/np.sqrt(2), 245/np.sqrt(2)],
        #     [0.0, 122.5/np.sqrt(2), 0]
        # ])
        ### default nodes ^^^

        curve1 = bezier.Curve(nodes,degree=degree)
        # print(curve1.implicitize())

        def curve(x):
            return -173.2412/30012.5 * x**2 + x

        x_axis = np.linspace(0,245/np.sqrt(2),50)
        z_axis = curve(x_axis)

        plt.scatter(x_axis,z_axis,marker='o',color ='r')

        curve1.plot(100,ax=plt)

        plt.show()

        return x_axis,z_axis
    

    def inverse_kinematics(x_coordinate,z_coordinate):


        return


Kine = Kinematics_class()
x,z = Kine.bezier_generate()

