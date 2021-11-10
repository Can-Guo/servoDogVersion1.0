'''
Date: 2021-11-09 16:29:29
LastEditors: Guo Yuqin,12032421@mail.sustech.edu.cn
LastEditTime: 2021-11-10 21:58:11
FilePath: /IMU_Python_Reading/Python_multiThread/XBOX_threading_test.py
'''

from queue import Queue 
from threading import Thread 
from Xbox_value import XBOX_class 
import numpy as np 


## create a thread to access the XBOX status
def XBOX_access(output_queue_1):
    print("Thread - 1 ")
    XBOX_device = XBOX_class()
    XBOX_device.initialize_xbox()

    while True:
        command = XBOX_device.get_xbox_status()
        output_queue_1.put(command)
    
## create a thread to do somethiXBOX_deviceng based on the XBOX status

def XBOX_command(input_queue_1):
    print("Thread - 2 ")
    while True:
        command = input_queue_1.get()
        # print("Thread - 2 is running :",command)
    


if __name__ == '__main__':

    qq = Queue()

    t3 = Thread(target=XBOX_access,args=(qq,))
    t4 = Thread(target=XBOX_command,args=(qq,))

    t3.start()
    t4.start()


