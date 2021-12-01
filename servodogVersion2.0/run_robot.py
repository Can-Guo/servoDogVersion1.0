'''
Date: 2021-11-10 22:11:41
LastEditors: Guo Yuqin,12032421@mail.sustech.edu.cn
LastEditTime: 2021-12-02 04:38:24
FilePath: /servodogVersion2.0/run_robot.py
'''
import numpy as np
# import pigpio 
from Xbox_value import XBOX_class
from IMU_class import IMU_class 
from Hardware_Config import Hardware_Class


from queue import Queue 
from threading import Thread
import matplotlib.pyplot as plt

from initial_pwm import POWER 
import time 

## Two Thread for XBOX 

## create a thread to access the XBOX status

def XBOX_access(output_queue_1):
    # print("Thread - 3 - XBOX access")
    XBOX_device = XBOX_class()
    XBOX_device.initialize_xbox()

    while True:
        command = XBOX_device.get_xbox_status()
        output_queue_1.put(command)

        if stop_threads == True:
            break
    
### create a thread to do something  based on the XBOX status

def XBOX_command(input_queue_1):
    # print("Thread - 4 - XBOX command")
    Hardware = Hardware_Class()
    # Hardware.initialize_leg_pwm()
    
    Hardware.initialize_usrl_pwm()
    time.sleep(5)
    
    Hardware.usrl_pwm.T200_power_scale = POWER[2]

    # Hardware.send_io_pwm(20,1560)
    # Hardware.send_io_pwm(21,1560)

    while True:
        command = input_queue_1.get()

        ### USRL servo control based on XYAB buttons
        ## Angle:       0  -- 180  --  360 (deg)
        ## Pulse Width: 500 - 1500  -- 2500 (us)
        ### 

        # if command.X == 1: 
        #     Hardware.pi.set_servo_pulsewidth(Hardware.usrl_pwm.servo_pins[0],2000)
        #     Hardware.pi.set_servo_pulsewidth(Hardware.usrl_pwm.servo_pins[1],1500)

        #     print("X:",command.X)
        # elif command.A == 1:
        #     Hardware.pi.set_servo_pulsewidth(Hardware.usrl_pwm.servo_pins[0],1500)
        #     Hardware.pi.set_servo_pulsewidth(Hardware.usrl_pwm.servo_pins[1],2000)
        #     print("A:",command.A)
        # elif command.B == 1:
        #     Hardware.pi.set_servo_pulsewidth(Hardware.usrl_pwm.servo_pins[0],1000)
        #     Hardware.pi.set_servo_pulsewidth(Hardware.usrl_pwm.servo_pins[1],500)
        #     print("B:",command.B)
        # elif command.Y == 1:
        #     Hardware.pi.set_servo_pulsewidth(Hardware.usrl_pwm.servo_pins[0],500)
        #     Hardware.pi.set_servo_pulsewidth(Hardware.usrl_pwm.servo_pins[1],1000)
        #     print("Y:",command.Y)
        print("Angle:",(command.usrl_servo_command))
        if 360.0 > command.usrl_servo_command >= 180.0:
            servo_0 = (int) (500 + (command.usrl_servo_command - 180) * (1000 / 180.0))
            servo_1 = (int) (2500 - (command.usrl_servo_command - 180) * (1000 / 180.0))
        elif 180.0 > command.usrl_servo_command >= 0.0:
            servo_0 = (int) (1500 + command.usrl_servo_command * (1000 / 180.0))
            servo_1 = (int) (1500 - command.usrl_servo_command * (1000 / 180.0))
        
        print("Servo 1 %d \t Servo 2 %d \t" % (servo_0,servo_1))

        Hardware.pi.set_servo_pulsewidth(Hardware.usrl_pwm.servo_pins[0],servo_0)
        Hardware.pi.set_servo_pulsewidth(Hardware.usrl_pwm.servo_pins[1],servo_1)
        # Hardware.pi.set_servo_pulsewidth(Hardware.usrl_pwm.servo_pins[1],1500)
        # Hardware.pi.set_servo_pulsewidth(Hardware.usrl_pwm.servo_pins[1],1500)

        

        

        ### USRL T200 control based on the value of L_step
        # -1 ->  0  ->   1
        # zero force ->  half power  ->  full power
        # 1500  ->  1700  ->  1900
        # Power scaler is a constant used to limited the power of the T200

        Power = Hardware.usrl_pwm.T200_power_scale
        print("Power:",Power)

        if command.L_step == 0 :
            Pwm = (int)(1500 + (200 * Power))
        else:
            Pwm = (int)(1500 + (command.L_step + 1) * (400/2.0) * Power)
        pass


        # print("PWM:",(int)(Pwm))

        for i in range(2):
            Hardware.send_io_pwm_width(Hardware.usrl_pwm.T200_pins[i],Pwm)

        # time.sleep(5)

        # Hardware.send_io_pwm(21,Pwm)
        
        if stop_threads == True:
            break

        # print("Thread - 2 is running :",command)
        # return command



#### Two Thread for IMU data reading and plotting


q_lines = []

### Create a data producer, such as acquire the data from IMU sensor

def IMU_data_producer(output_queue):
    # print("Thread 2 - IMU data producer")
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

        if stop_threads == True:
            break
    
    
## Create a data consumer, such as plotting the IMU data

def IMU_plotting(input_queue):
    # print("Thread 1 - XBOX data access")

    angles = input_queue.get()
        
        # update the figure with the IMU data
    
    # for i in range(3):
    #     q_lines[i].set_ydata(angles[:,i])

    # plt.draw()
    # plt.pause(0.001)
    
    return angles




def main():

    global times
    times = 200
    global q_lines
    global stop_threads
    stop_threads = False

    # initialize the IMU data
    q_init = np.zeros([1000,3])
    angle_name = ['Roll','Pitch','Yaw']


    fig = plt.figure(figsize=(12,8))

    for i in range(3):
        plt.subplot(3,1,i+1)
        if i == 0:
            q_line, = plt.plot(q_init[:,i],'r-')
        elif i == 1:
            q_line, = plt.plot(q_init[:,i],'b-')
        elif i == 2:
            q_line, = plt.plot(q_init[:,i],'g-')
            
        q_lines.append(q_line)
        plt.ylabel('{}/deg'.format(angle_name[i]))
        plt.ylim([-180,180])

    plt.xlabel('IMU data frames')
    fig.legend(['IMU data'],loc='upper center')
    fig.tight_layout()
    plt.draw()  

    ### Create FIFO Queue for mult-threading 
    q1 = Queue()
    t1 = Thread(target=IMU_plotting,args=(q1,))
    t2 = Thread(target=IMU_data_producer,args=(q1,))

    q2 = Queue()
    t3 = Thread(target=XBOX_access,args=(q2,))
    t4 = Thread(target=XBOX_command,args=(q2,))

    # pi = pigpio.pi()

    ### Start multi-threading
    t1.start()
    t2.start()

    t3.start()
    t4.start()

    ### main Thread -- update the figure for IMU data plotting
    tick1 = time.time()

    for i in range(times):

        angle = IMU_plotting(input_queue=q1)
        # print("Angle type:",type(angle))
        # print("Q_lines type:",type(q_lines))

        for i in range(3):
            q_lines[i].set_ydata(angle[:,i])

        plt.draw()
        plt.pause(0.0001)

        if i == times-1:
            stop_threads = True

        if stop_threads == True:
            break

    tick2 = time.time()

    print("Running Time:",tick2-tick1)

main()
