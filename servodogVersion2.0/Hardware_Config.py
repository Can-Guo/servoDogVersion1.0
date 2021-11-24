'''
Date: 2021-11-10 22:44:35
LastEditors: Guo Yuqin,12032421@mail.sustech.edu.cn
LastEditTime: 2021-11-25 02:36:55
FilePath: /servodogVersion2.0/Hardware_Config.py
'''
from numpy.core.defchararray import not_equal
import pigpio 
from initial_pwm import Leg_PWM_Parameter, USRL_PWM_Parameter
import time 
class Hardware_Class:
    def __init__(self):
        # Before you config, run "sudo pigpiod" in your terminal

        self.pi = pigpio.pi()

        self.leg_pwm = Leg_PWM_Parameter()
        self.usrl_pwm = USRL_PWM_Parameter()

    
    def initialize_leg_pwm(self):
        for leg_index in range(4):
            for axis_index in range(3):
                self.pi.set_PWM_frequency(
                    self.leg_pwm.leg_pins[axis_index, leg_index], self.leg_pwm.leg_frequency
                )
                self.pi.set_PWM_range(
                    self.leg_pwm.leg_pins[axis_index, leg_index], self.leg_pwm.leg_range
                )
                self.pi.set_servo_pulsewidth(
                    self.leg_pwm.leg_pins[axis_index, leg_index], self.leg_pwm.leg_home_position[axis_index,leg_index]
                )
        time.sleep(2)
        return 
    

    def initialize_usrl_pwm(self):
        for i in range(2):
            self.pi.set_PWM_frequency(self.usrl_pwm.T200_pins[i],self.usrl_pwm.T200_frequency)
            self.pi.set_PWM_range(self.usrl_pwm.T200_pins[i],self.usrl_pwm.T200_range)            
            self.pi.set_servo_pulsewidth(self.usrl_pwm.T200_pins[i],self.usrl_pwm.T200_home_position[i])

        for i in range(2):
            self.pi.set_PWM_frequency(self.usrl_pwm.servo_pins[i],self.usrl_pwm.servo_frequency)
            self.pi.set_PWM_range(self.usrl_pwm.servo_pins[i],self.usrl_pwm.servo_range)            
            self.pi.set_servo_pulsewidth(self.usrl_pwm.servo_pins[i],self.usrl_pwm.servo_home_position[i])
        
        return

    
    def send_io_pwm_width(self,PIN_io,pulse_width):
        pulse_width = int(pulse_width)
        self.pi.set_servo_pulsewidth(PIN_io,pulse_width)

        return 
        
    def send_leg_pwm_width(self,pulse_width):
        pulse_width = int(pulse_width)
        for leg_index in range(4):
            for axis_index in range(3):
                self.pi.set_servo_pulsewidth(
                    self.leg_pwm.leg_pins[axis_index, leg_index], pulse_width[axis_index,leg_index]
                )

        return 


    def send_T200_pwm_width(self,pulse_width):
        pulse_width = int(pulse_width)
        for i in range(2):
            self.pi.set_servo_pulsewidth(
                self.usrl_pwm.T200_pins[i],pulse_width[i]
            )

        return 
    
    def send_servo_pwm_width(self,pulse_width):
        pulse_width = int(pulse_width)
        for i in range(2):
            self.pi.set_servo_pulsewidth(
                self.usrl_pwm.servo_pins[i],pulse_width[i]
            )

        return 


    def angle_2_duty_cycle(angle):
        
        ''' for Xunlongzhe Servo 
        deg :   0 --- 180 --- 360 (deg)
        duty:   5% -- 15% --- 25% (deg)
        '''

        return 


    def angle_delta_2_pulse_width(self,angle_delta=0):

        ''' for Xunlongzhe Servo 
        deg :   0 --- 180 --- 360 (deg)
        width:  500 - 1500 -- 2500 (us)
        '''

        return (int)(angle_delta * 1000 / 180)


    def force_2_pulse_width(force):
        ''' for T200 Thruster
        deg :   0 --- 180 --- 360 (deg)
        width:  500 - 1500 -- 2500 (us)
        '''

        return 



## standing with home position

Hardware = Hardware_Class()
Hardware.initialize_leg_pwm()

## leg locomotion after initialize the leg position
import numpy as np 
from Kinematics import Kinematics_class

Kinematics = Kinematics_class()

# 1. generate a bezier trajectory
x,z = Kinematics.bezier_generate()
x_leg = x - 120/np.sqrt(2)
z_leg = z - 240/np.sqrt(2) 


# 2. inverse kinematics to get the joint angle of the leg

q2_list = []
q3_list = []

for i in range(50):
    q2,q3 = Kinematics.inverse_kinematics_geo(x_leg[i],-60,z_leg[i])
    q2_list.append(q2*180/np.pi)
    q3_list.append(q3*180/np.pi)

# 3. compute the delta(pulse width) compare to the home position of joints

q2_pulse_width_delta = []
q3_pulse_width_delta = []

for i in range(len(q2_list)):
    q2_pulse_width_delta.append(1500+Hardware.angle_delta_2_pulse_width(q2_list[i]))
    q3_pulse_width_delta.append(780+Hardware.angle_delta_2_pulse_width(q3_list[i]))

# print("q2",q2_pulse_width_delta)
# print("q3",q3_pulse_width_delta)

# for i in range(len(q2_pulse_width_delta)):
#     Hardware.send_io_pwm_width(24,q2_pulse_width_delta[i])
#     Hardware.send_io_pwm_width(25,q3_pulse_width_delta[i])
#     time.sleep(0.25)

# for i in range(len(q2_pulse_width_delta)):
#     Hardware.send_io_pwm_width(3,q2_pulse_width_delta[i])
#     Hardware.send_io_pwm_width(4,q3_pulse_width_delta[i])
#     time.sleep(0.1)

# for i in range(len(q2_pulse_width_delta)):
#     Hardware.send_io_pwm_width(15,q2_pulse_width_delta[i])
#     Hardware.send_io_pwm_width(17,q3_pulse_width_delta[i])
#     time.sleep(0.4)



# print(q2_pulse_width_delta)




