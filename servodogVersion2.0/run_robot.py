'''
Date: 2021-11-10 22:11:41
LastEditors: Guo Yuqin,12032421@mail.sustech.edu.cn
LastEditTime: 2021-11-11 01:58:29
FilePath: /servodogVersion2.0/run_robot.py
'''
import numpy as np 
import pigpio 
from Xbox_value import XBOX_class
from IMU_class import IMU_class 
from Hardware_Config import Hardware_Class


from queue import Queue 
from threading import Thread
import matplotlib.pyplot as plt

from initial_pwm import POWER 

## Two Thread for XBOX 

## create a thread to access the XBOX status

def XBOX_access(output_queue_1):
    print("Thread - 1 ")
    XBOX_device = XBOX_class()
    XBOX_device.initialize_xbox()

    while True:
        command = XBOX_device.get_xbox_status()
        output_queue_1.put(command)
    
## create a thread to do something  based on the XBOX status

def XBOX_command(input_queue_1):
    print("Thread - 2 ")
    Hardware = Hardware_Class()
    Hardware.initialize_leg_pwm()
    Hardware.initialize_usrl_pwm()
    
    Hardware.usrl_pwm.T200_power_scale = POWER[3]

    while True:
        command = input_queue_1.get()

        ### USRL servo control based on XYAB buttons
        ## Angle:       0  -- 180  --  360 (deg)
        ## Pulse Width: 500 - 1500  -- 2500 (us)
        ### 

        if command.X == 1: 
            Hardware.pi.set_servo_pulsewidth(Hardware.usrl_pwm.servo_pins[0],500)
            print("X:",command.X)
        if command.A == 1:
            Hardware.pi.set_servo_pulsewidth(Hardware.usrl_pwm.servo_pins[0],1000)
            print("A:",command.A)
        if command.B == 1:
            Hardware.pi.set_servo_pulsewidth(Hardware.usrl_pwm.servo_pins[0],1500)
            print("B:",command.B)
        if command.Y == 1:
            Hardware.pi.set_servo_pulsewidth(Hardware.usrl_pwm.servo_pins[0],2500)
            print("Y:",command.Y)

        ### USRL T200 control based on the value of L_step
        # -1 ->  0  ->   1
        # zero force ->  half power  ->  full power
        # 1500  ->  1700  ->  1900
        # Power scaler is a constant used to limited the power of the T200

        Power = Hardware.usrl_pwm.T200_power_scale
        print("Power:",Power)

        if command.L_step == 0 :
            Pwm = 1500 + 200 * Power
        else:
            Pwm = 1500 + (command.L_step + 1) * (400/2.0) * Power

        print("PWM:",Pwm)

        for i in range(2):
            Hardware.send_io_pwm(Hardware.usrl_pwm.T200_pins[i],Pwm)


        # print("Thread - 2 is running :",command)



#### Two Thread for IMU data reading and plotting


q_lines = []

## Create a data producer, such as acquire the data from IMU sensor

def IMU_data_producer(output_queue):
    
    angle_list = np.zeros([1000,3])

    # Initialize the IMU class
    IMU_device = IMU_class()

    while True:
        # Acquire the IMU data
        Angles = IMU_device.get_IMU_data()

        # print(Angles)
        
        # re-arrange the data shape
        angle_list[:-1] = angle_list[1:]
        angle_list[-1] = Angles

        
        # Put out the data for IMU_plotting threading
        output_queue.put(angle_list)
    
    
## Create a data consumer, such as plotting the IMU data

def IMU_plotting(input_queue):
    global q_lines 

    # initialize the IMU data
    q_init = np.zeros([1000,3])
    angle_name = ['Roll','Pitch','Yaw']


    fig = plt.figure(figsize=(12,8))

    for i in range(3):
        plt.subplot(3,1,i+1)
        q_line, = plt.plot(q_init[:,i],'-')
        q_lines.append(q_line)
        plt.ylabel('{}/deg'.format(angle_name[i]))
        plt.ylim([-180,180])

    plt.xlabel('simulation steps')
    fig.legend([''],loc='lower center')
    fig.tight_layout()
    plt.draw()


    

    while True:
        # retrieve IMU data
        angles = input_queue.get()
        
        # update the figure with the IMU data
    
        for i in range(3):
            q_lines[i].set_ydata(angles[:,i])

        plt.draw()
        plt.pause(0.001)




def main():
    

    q = Queue()
    # t1 = Thread(target=IMU_plotting,args=(q,))
    # t2 = Thread(target=IMU_data_producer,args=(q,))

    t3 = Thread(target=XBOX_access,args=(q,))
    t4 = Thread(target=XBOX_command,args=(q,))

    # pi = pigpio.pi()


    # t1.start()
    # t2.start()
    t3.start()
    t4.start()


main()