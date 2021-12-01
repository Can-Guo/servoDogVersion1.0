'''
Date: 2021-11-10 23:18:34
LastEditors: Guo Yuqin,12032421@mail.sustech.edu.cn
LastEditTime: 2021-11-25 01:19:17
FilePath: /servodogVersion2.0/Kinematics.py
'''
## TODO:  Kinematics(forward and inverse) for USRL robot
## Data: 20211110 - 20211117

import matplotlib.pyplot as plt
import numpy as np 
import math
import bezier
import sympy


class Kinematics_class():

    def __init__(self):
        
        self.L1 = 60
        self.L2 = 120
        self.L3 = 120
        
        


    def bezier_generate(self):
        ### default nodes: 
        # nodes1 = np.asfortranarray([
        #     [0.0, 122.5/np.sqrt(2), 245/np.sqrt(2)],
        #     [0.0, 122.5/np.sqrt(2), 0]
        # ])
        ### default nodes ^^^

        nodes1=np.asfortranarray([
            [0.0, 120/np.sqrt(2), 240/np.sqrt(2)],
            [0.0, 120/np.sqrt(2), 0.0           ],
            ])
        degree1=2

        curve1 = bezier.Curve(nodes1,degree1)
        # print(curve1.implicitize())

        def curve(x):
            # -a * (b*x**2 - a*x + a*y)/c = 0
            # -5970985942992911*(35184372088832*x**2 - 5970985942992911*x + 5970985942992911*y)/1237940039285380274899124224
            
            # return -173.2412/30012.5 * x**2 + x
            return -1/169.70562748477138 * x**2 + x
            

        x_axis = np.linspace(0,240/np.sqrt(2),50)
        z_axis = curve(x_axis)

        plt.figure(figsize=(8,8))
        plt.scatter(x_axis,z_axis,marker='o',color ='r')

        curve1.plot(100,color = 'b',ax=plt)


        return x_axis,z_axis
    
    def forward_kinematics_2R(self,q2,q3):
        '''
        input: theta_2,theta_3 of the 2R-link leg model, assumed theta_1(hip) is fixed.
        output: x and z coordinates of the trajectory points, limite the locomotion to XZ plane
        '''
        if   0<q2<np.pi/2 and 0<q2+q3<np.pi/2:
            X = (self.L2*np.cos(q2) + self.L3*np.cos(q2+q3))
            Z = (self.L2*np.sin(q2) + self.L3*np.sin(q2+q3))
        elif 0<q2<np.pi/2 and np.pi/2<q2+q3<np.pi:              
            X = (self.L2*np.cos(q2) - self.L3*np.sin(q2+q3-np.pi/2))
            Z = (self.L2*np.sin(q2) + self.L3*np.sin(q2+q3))
        elif np.pi/2<q2<np.pi and np.pi/2<q2+q3<np.pi:
            X = -(self.L2*np.sin(q2-np.pi/2) + self.L3*np.sin(q2+q3-np.pi/2))
            Z =  (self.L2*np.cos(q2-np.pi/2) + self.L3*np.cos(q2+q3-np.pi/2))
        elif np.pi/2<q2<np.pi and np.pi<q2+q3<3*np.pi/2:
            X = -(self.L2*np.sin(q2-np.pi/2) + self.L3*np.cos(q2+q3-np.pi))
            Z =  (self.L2*np.cos(q2-np.pi/2) - self.L3*np.sin(q2+q3-np.pi))
        else:
            print("Waring! Unexpected joint angles!")

        return -X,-Z

    def inverse_kinematics(self,x_coordinate=None,y_coordinate = -60,z_coordinate=None):
        '''
        https://github.com/Shihao-Feng-98/Quadruped_FSH/blob/main/src/leg_kinematics.py
        Description: Inverse kinematics of 2-Link leg
        Input: p -> foot position, 1d array (3,)
        Output: q -> joint angle, 1d array (3,)
        '''
        p = np.array([x_coordinate,y_coordinate,z_coordinate])

        L1 = self.L1; L2 = self.L2; L3 = self.L3
        L_yz = np.sqrt(p[1]**2 + p[2]**2 - L1**2)
        L_xz_pie = np.sqrt(L_yz**2 + p[0]**2)
        n = (L_xz_pie**2 - L3**2 - L2**2) / (2*L2)
        q1 = - np.arctan(p[1] / p[2]) - np.arctan(L1 / L_yz)
        q2 = - np.arctan(p[0] / L_yz) + np.arccos((L2 + n) / L_xz_pie)
        q3 = - np.arccos(n / L3)
        q = np.array([q1, q2, q3]) # (3,)        
        return q

    def inverse_kinematics_geo(self,x=None,y=-60,z = None):
        '''
        input: x and z coordinates of the trajectory points, limite the locomotion to XZ plane
        output: theta_2,theta_3 of the 2R-link leg model, assumed theta_1(hip) is fixed.
        '''

        if (np.sqrt(x**2+z**2) > (self.L2 + self.L3)):
            print("This point is out of workspace of the robot")
            pass
        # elif (np.sqrt(x**2+z**2) < (self.L2)):
            # print("Warning! This point is not recommend! Please reconsider another point!")
            # pass
        elif z>0:
            print("Warning! z>0! This point is not recommend! Please reconsider another point!")
            pass
        else:
            L_xz = np.sqrt(x**2+z**2)
            L2 = self.L2
            L3 = self.L3

            if x>0:
                beta_pie = np.arctan2(-z,x)
                # print(beta_pie*180/np.pi)
                beta = np.pi/2 - beta_pie
                
                phi = np.arccos((L_xz**2 + L2**2 - L3**2)/(2*L2*L_xz))

                if 0<phi<np.pi:
                    q2_real = np.pi/2 + beta - phi  ## common elbow
                else:   ## inverse elbow for unexpected case
                    print("Warning! Unexpected phi angle!")

                q3 = np.arccos((L_xz**2 - L2**2 - L3**2)/(2*L2*L3))

                if q3<0:  ## inverse elbow for unexpected case
                    q3_real = - q3
                elif q3>0:     ## common elbow
                    q3_real = q3

            elif x<=0:
                if x == 0:
                    beta = np.pi/2
                else:
                    tanvalue = z/x
                    beta = np.arctan(tanvalue)
                    
                # print(beta*180/np.pi)
                phi = np.arccos((L_xz**2 + L2**2 - L3**2)/(2*L2*L_xz))
                # print(phi*180/np.pi)

                if 0<phi<np.pi:
                    q2_real = beta - phi    ## common elbow
                else:   ## inverse elbow for unexpected case
                    print("Warning! Unexpected phi angle!")

                q3 = np.arccos((L_xz**2 - L2**2 - L3**2)/(2*L2*L3))
                # print("q3",q3*180/np.pi)

                if q3<0:  ## inverse elbow for unexpected case
                    q3_real = - q3
                elif q3>0:     ## common elbow
                    q3_real = q3
            
            
            return q2_real,q3_real


    def circle(self,R,theta_start,theta_end):
        nums = (int)(theta_end-theta_start)/(np.pi/120)
        theta = np.linspace(theta_start,theta_end,100)
        x = R * np.cos(theta)
        y = R * np.sin(theta)
        plt.plot(x,y,'g--')
        return x,y


#############################################
# Test the Kinematics Class --> BEGIN


Kine = Kinematics_class()
x,z = Kine.bezier_generate()
x_leg = x - 120/np.sqrt(2)
z_leg = z - 240/np.sqrt(2) + 10

plt.plot(x_leg,z_leg,'c-')
Kine.circle(120,0,2*np.pi)
Kine.circle(240,0,2*np.pi)

x_plot = []
z_plot = []
q2_plot = []
q3_plot = []

for i in range(50):
    q2,q3 = Kine.inverse_kinematics_geo(x_leg[i],-60,z_leg[i])
    q2_plot.append(q2*180/np.pi)
    q3_plot.append(q3*180/np.pi)
    x1,z1 = Kine.forward_kinematics_2R(q2,q3)
    x_plot.append(x1)
    z_plot.append(z1)

plt.scatter(x_plot,z_plot,marker='*',color ='g')
t = np.linspace(1,51,50)

plt.plot(t,q2_plot,'b-.')
plt.plot(t,q3_plot,'y-.')
plt.show()

# Test the Kinematics Class --> END
############################################# 




