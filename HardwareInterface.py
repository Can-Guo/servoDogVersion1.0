import numpy
import pigpio 
from PWM_config import Servo_PWM_Parameter, Thruster_PWM_Para
import os 
import time 

class HardwareInterface:
    def __init__(self):
        open_io = "sudo pigpiod"
        os.system(open_io)
        time.sleep(1)
        self.pi = pigpio.pi()
        self.servo_pwm_params = Servo_PWM_Parameter()
        self.thruster_pwm_params = Thruster_PWM_Para()
        initialize_pwm(self.pi, self.servo_pwm_params)
        initialize_pwm(self.pi, self.thruster_pwm_params)
    
    def set_actuator_positions(self, joint_angles):
        send_servo_commands(self.pi, self.servo_pwm_params, joint_angles)
    
    def set_thruster_positions(self, imu_information):
        pass

def initialize_pwm(pi, pwm_params):
    for leg_index in range(4):
        for axis_index in range(3):
            pi.set_PWM_frequency(
                pwm_params.pins[axis_index, leg_index], pwm_params.freq
            )
            pi.set_PWM_range(pwm_params.pins[axis_index, leg_index], pwm_params.range)

def send_servo_commands(pi, servo_pwm_params, joint_angles):
    for leg_index in range(4):
        for axis_index in range(3):
            pulse_width = joint_deg_to_pulse_width(
                joint_angles[axis_index, leg_index],
                servo_pwm_params,
                axis_index,
                leg_index,
            )
            pi.set_servo_pulsewidth(servo_pwm_params.pins[axis_index, leg_index], pulse_width[leg_index,axis_index])


def joint_deg_to_pulse_width(joint_angles,pulse_width,axis_index,leg_index):
    # according to the mannual of servo motor by XUNLONGZHE.com
    # url : https://item.taobao.com/item.htm?spm=a1z10.5-c-s.w4002-17909957398.71.cd013fdd6F6uHw&id=616071138320
    pulse_width[axis_index,leg_index] = 2.0 * joint_angles[axis_index,leg_index] / 360.0 + 0.5

def deactivate_servos(pi, pwm_params):
    # dutycycle --> 0 
    for leg_index in range(4):
        for axis_index in range(3):
            pi.set_PWM_dutycycle(pwm_params.pin[axis_index, leg_index], 0)

def deg_to_radian(deg):
    return deg / 180.0 * numpy.pi

def radian_to_deg(radian):
    return radian / numpy.pi * 180.0