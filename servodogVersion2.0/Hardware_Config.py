'''
Date: 2021-11-10 22:44:35
LastEditors: Guo Yuqin,12032421@mail.sustech.edu.cn
LastEditTime: 2021-11-17 22:29:11
FilePath: /servodogVersion2.0/Hardware_Config.py
'''
from numpy.core.defchararray import not_equal
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
                self.pi.set_servo_pulsewidth(
                    self.leg_pwm.leg_pins[axis_index, leg_index], self.leg_pwm.leg_home_position[axis_index,leg_index]
                )
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



# ## standing with home position

Hardware = Hardware_Class()

# while True:
Hardware.initialize_leg_pwm()

