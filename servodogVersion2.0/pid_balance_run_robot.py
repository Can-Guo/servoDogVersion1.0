'''
*********************************************************************************************
  *File: pid_balance_run_robot.py
  *Project: servodogVersion2.0
  *Filepath: /home/guoyucan/ServoDogVersion1.0/servodogVersion2.0/pid_balance_run_robot.py 
  *File Created: Friday, 10th December 2021 09:30:01 am
  *Author: Guo Yucan, 12032421@mail.sustech.edu.cn 
  *Last Modified: Wednesday, 15th December 2021 10:00:05 pm
  *Modified By: Guo Yucan, 12032421@mail.sustech.edu.cn 
  *Copyright @ 2021 , BionicDL LAB, SUSTECH, Shenzhen, China 
*********************************************************************************************
'''

import numpy as np 
from IMU_class import IMU_class
from Hardware_Config import Hardware_Class

from queue import Queue
from threading import Thread
import matplotlib.pyplot as plt 
import time 

from initial_pwm import POWER 

## Two thread for IMU 

# create a thread to access the XBOX status

### Two thread for IMU data reading and plotting 

q_lines = []

# create a data producer, such as acquire the data from IMU device

def IMU_data_producer(output_queue):


    angle_list = np.zeros([1000,3])
    omega_list = np.zeros([1000,3])
    
    time_sequence = []
    

    # initialize the IMU class
    IMU_device = IMU_class()

    Angle_and_time = IMU_device.get_IMU_data()
    time_sequence.append(Angle_and_time[3])


    while True:

        # Acquire the IMU data
        Angle_and_time = IMU_device.get_IMU_data()
        Angles_now = Angle_and_time[:3]

        time_last = time_sequence[-1]

        time_now = Angle_and_time[3]

        # print("time_now",(time_now))
        # print("time delta", (time_now - time_last).total_seconds())
        time_sequence.append(time_now)


        # re-arrange the data shape
        angle_list[:-1] = angle_list[1:]
        Angles_last = angle_list[-2]
        angle_list[-1] = Angles_now

        # print("(Angles_now - Angles_last)",(Angles_now - Angles_last))

        omega_list[:-1] = omega_list[1:]
        omega_list[-1] = ((Angles_now - Angles_last)/((time_now-time_last).total_seconds()))
        # print("omega list",omega_list[-1])

        # put out the data for IMU_plotting threading
        angle_omega = [angle_list, omega_list]
        # output_queue.put(angle_list, omega_list)
        output_queue.put(angle_omega)

    # if stop_threads == True:
    #     break

## Create a data consumer, such as plotting the IMU data

def IMU_plotting(input_queue):

    angle = (input_queue.get())[0]
    omega = (input_queue.get())[1]

    return angle, omega


if __name__ == '__main__':

    ## 
    Hardware = Hardware_Class()
    # Hardware.initialize_leg_pwm()
    
    Hardware.initialize_usrl_pwm()
    time.sleep(5)
    
    Hardware.usrl_pwm.T200_power_scale = POWER[2]



    global times
    times = 200

    global stop_threads
    stop_threads = False

    # initialize the IMU data 
    q_init = np.zeros([1000,6])
    ylabel_name = ['Roll','Pitch','Yaw', 'omega_x', 'omega_y', 'omega_z']

    # initialize Plot figure
    fig = plt.figure(figsize=(12,8))

    for i in range(6):
        plt.subplot(6,1,i+1)
        if i == 0:
            q_line, = plt.plot(q_init[:,i],'r-')
        elif i == 1:
            q_line, = plt.plot(q_init[:,i],'b-')
        elif i == 2:
            q_line, = plt.plot(q_init[:,i],'g-')

        if i == 3:
            q_line, = plt.plot(q_init[:,i],'c-.')
        elif i == 4:
            q_line, = plt.plot(q_init[:,i],'k-.')
        elif i == 5:
            q_line, = plt.plot(q_init[:,i],'y-.')

        q_lines.append(q_line)
        if(i<3):
            plt.ylabel('{}/deg'.format(ylabel_name[i]))
        else:
            plt.ylabel('{}/(deg/s)'.format(ylabel_name[i]))
        plt.ylim([-180,180])

    plt.xlabel('IMU data frames')
    fig.legend(['IMU data'],loc='upper center')
    fig.tight_layout()
    plt.draw()


    ### Create FIFO Queue for mult-threading 
    q1 = Queue()
    t1 = Thread(target=IMU_plotting,args=(q1,))
    t2 = Thread(target=IMU_data_producer,args=(q1,))

    ### Start multi-threading
    t1.start()
    t2.start()

    ### main thread -- update the figure for IMU data plotting

    Kp = 1.0
    Kd = 0.1

    for i in range(times):

        angle, omega = IMU_plotting(input_queue=q1)

        # print("Angle type:",type(angle))
        # print("Q_lines type:",type(q_lines))

        for i in range(3):
            q_lines[i].set_ydata(angle[:,i])
        
        for i in range(3,6):
            q_lines[i].set_ydata(omega[:,i-3])
        

        plt.draw()
        plt.pause(0.001)


        Power = Hardware.usrl_pwm.T200_power_scale
        print("Power Scaler:",Power)
        

        pitch_last = angle[-2,1]
        pitch_now  = angle[-1,1]

        omega_y_last = omega[-2,1]
        omega_y_now  = omega[-1,1]


        Pwm_delta = Kp * (pitch_now - pitch_last) + Kd * (omega_y_now - omega_y_last)

        print("Pwm_delta", Pwm_delta)

        if( np.abs(pitch_now - 0.0) < 5.0 ):
            Pwm = 1500
        elif( pitch_now > 0 ):
            Pwm = (int) (1500 + Pwm_delta * Power)
        elif( pitch_now < 0 ):
            Pwm = (int) (1500 - Pwm_delta * Power)
        else:
            pass

        print("Pwm:", Pwm)
        
        # Safe Protection for PWM range
        if( Pwm > 1700):
            Pwm = 1700
        if( Pwm < 1300):
            Pwm = 1300

        for i in range(2):
            Hardware.send_io_pwm_width(Hardware.usrl_pwm.T200_pins[i],Pwm)


        if i == times-1:
            stop_threads = True

        if stop_threads == True:
            break
