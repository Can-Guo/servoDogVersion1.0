'''
Date: 2021-11-10 22:44:35
LastEditors: Guo Yuqin,12032421@mail.sustech.edu.cn
LastEditTime: 2021-11-11 01:25:19
FilePath: /servodogVersion2.0/Hardware_Config.py
'''
import pigpio 
from initial_pwm import Leg_PWM_Parameter, USRL_PWM_Parameter

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
        return 
    

    def initialize_usrl_pwm(self):
        for i in range(2):
            self.pi.set_PWM_frequency(self.usrl_pwm.T200_pins[i],self.usrl_pwm.T200_frequency)
            self.pi.set_PWM_range(self.usrl_pwm.T200_pins[i],self.usrl_pwm.T200_range)            

        for i in range(2):
            self.pi.set_PWM_frequency(self.usrl_pwm.servo_pins[i],self.usrl_pwm.servo_frequency)
            self.pi.set_PWM_range(self.usrl_pwm.servo_pins[i],self.usrl_pwm.servo_range)            

        return            

    
    def send_io_pwm(self,PIN,Pulse_width):
        self.pi.set_servo_pulsewidth(PIN,Pulse_width)

        return
        
    def send_leg_pwm(self):

        return


    def send_T200_pwm(self):

        return 


    def angle_2_duty_cycle(angle):
        
        '''
        deg :   0 --- 180 --- 360 (deg)
        duty:   5% -- 15% --- 25% (deg)
        width:  500 - 1500 -- 2500 (us)
        '''

        return 


    def angle_2_pulse_width(angle):

        return 


    def force_2_pulse_width(force):


        return


