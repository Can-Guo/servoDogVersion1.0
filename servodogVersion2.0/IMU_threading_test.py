'''
*********************************************************************************************
  *File: IMU_threading_test.py
  *Project: Python_multiThread
  *Filepath: /home/guoyucan/BionicDL/Python_multiThread/IMU_threading_test.py 
  *File Created: Tuesday, 9th November 2021 10:36:35 am
  *Author: Guo Yucan, 12032421@mail.sustech.edu.cn 
  *Last Modified: Tuesday, 9th November 2021 10:36:39 am
  *Modified By: Guo Yucan, 12032421@mail.sustech.edu.cn 
  *Copyright @ 2021 , BionicDL LAB, SUSTECH, Shenzhen, China 
*********************************************************************************************
'''

from queue import Queue
from threading import Thread
# from Xbox_value import XBOX_class
from IMU_class import IMU_class 
import matplotlib.pyplot as plt 
import numpy as np 


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


if __name__ == '__main__':


    q = Queue()
    t1 = Thread(target=IMU_plotting,args=(q,))
    t2 = Thread(target=IMU_data_producer,args=(q,))

    t1.start()
    t2.start()
