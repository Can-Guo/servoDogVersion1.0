'''
Date: 2021-08-10 15:00:51
LastEditors: Guo Yuqin,12032421@mail.sustech.edu.cn
LastEditTime: 2021-08-12 11:22:33
FilePath: /servoDogVersion1.0/Xbox_value.py
Based on Source at pygame.joystick module demo -->
http://www.pygame.org/docs/ref/joystick.html
'''


## Functions of the class:
# This class can 
# 1. initialize the XBOX One Wireless controller 
# 2. access the axis, button & hat status of the joystick 
# 3. access the ID,GUID,name in system, power level of the joystick


import pygame


class XBOX_class:
    
    def __int__(self):
        
        # TODO: Define the function of the axes & buttons of the XBOX controller
    
        # ID of the joystick
        self.joystick = None
        self.name = None
        self.GUID = None
        
        # There are 6 axes in the XBOX joystick controller
        # axis_0,axis_1 --> left  stick
        # axis_3,axis_4 --> right stick
        # axis_2 --> Left trigger
        # axis_5 --> Right trigger
        
        self.axis_0 = 0.
        self.axis_1 = 0.
        self.L_step = -1.
        self.axis_3 = 0.
        self.axis_4 = 0.
        self.R_step = -1.

        # There are 11 buttons in the XBOX joystick controller
        self.A = 0 
        self.B = 0
        self.X = 0
        self.Y = 0

        self.LB = 0
        self.RB = 0
        self.View = 0
        self.Menu = 0
        self.Connect = 0

        # There is only one hat (0,0) in the XBOX joystick controller

        # hat_0 = (-1, 0) --> FX_left
        # hat_0 = (0 ,-1) --> FX_down
        # hat_0 = (0 , 1) --> FX_up
        # hat_0 = (1 , 0) --> FX_right
        
        self.FX_right = 0
        self.FX_left = 0
        self.FX_up = 0
        self.FX_down = 0

        
        # number of axes, buttons, hat(s)
        self.axes = 0
        self.buttons = 0
        self.hats = 0


        print("XBOX is Initializing ......")
        
        # self.initialize_xbox(self)


    def initialize_xbox(self):
        
        # Initialize the pyname module
        pygame.init()

        # Initialize the joystick sub-module
        pygame.joystick.init()

        # initialize the clock block
        # clock = pygame.time.Clock()

        # Initialize the joystick No.1, can integrated with more than 1 joystick
        joystick_count = pygame.joystick.get_count()

        if joystick_count == 1:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            self.name = self.joystick.get_name()

            print("Joystick ID : ",self.joystick)
            print("The Name of the Joystick : ",self.name)
        
        # Get the number of axes
        self.axes = self.joystick.get_numaxes()
        # print("number of axes:", self.axes)

        # Get the number of the buttons
        self.buttons = self.joystick.get_numbuttons()
        # print("number of buttons:",self.buttons)
        
        # Get the number of the hats
        self.hats = self.joystick.get_numhats()
        # print("number of hats:", self.hats)

        # Get the power level of the joystick
        self.power = self.joystick.get_power_level()
        print("Power Level : " , self.power)

        # Get the GUID of the joystick
        self.GUID = self.joystick.get_guid()
        print("GUID of the XBOX : " , self.GUID)

        print("Initialization of the XBOX is done!")

        
    def get_xbox_status(self):
        
        ## TODO: need to integrate with the stepless abjustment of Power 

 

        ### HAHAHA ! Interesting ! 
        self.done = False # Can be used to stop the scanning

        clock = pygame.time.Clock()

        while self.done == False:
            
            # self.initialize_xbox()
            # EVENT PROCESSING STEP
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self.done=True # Flag that we are done so we exit this loop
            

            # Get the status of the axes
            for i in range( self.axes ):
                axis = self.joystick.get_axis( i )
                # print(self.axes)
                if i == 0:
                    self.axis_0 = axis
                if i == 1:
                    self.axis_1 = axis
                if i == 2:
                    self.L_step = axis
                if i == 3:
                    self.axis_3 = axis
                if i == 4:
                    self.axis_4 = axis
                if i == 5:
                    self.R_step = axis

            # print("Stick 1  (%f,%f)  \n" % (self.axis_0, self.axis_1))
            # print(" Left_Step  %f  \n" % self.L_step)
            # print("Stick 2  (%f,%f)  \n" % (self.axis_3, self.axis_4))
            # print("Right_Step  %f  \n" % self.R_step)

            # Get the status of the buttons
            for i in range( self.buttons ):
                button = self.joystick.get_button( i )
                # print(i,button)
                if i == 0 and button == 1:
                    self.A = 1
                    print("A")
                if i == 1 and button == 1:
                    self.B = 1
                    print("B")
                if i == 2 and button == 1:
                    self.X = 1
                    print("X")
                if i == 3 and button == 1:
                    self.Y = 1
                    print("Y")
                if i == 4 and button == 1:
                    self.LB = 1
                    print("LB")
                if i == 5 and button == 1:
                    self.RB = 1
                    print("RB")
                if i == 6 and button == 1:
                    self.View = 1
                    print("View")
                if i == 7 and button == 1:
                    self.Menu = 1
                    print("Menu")
                if i == 8 and button == 1:
                    self.Connect = 1
                    print("Stop Connection !")
                    self.done = True


            for i in range( self.hats ):
                hat = self.joystick.get_hat( i )
                # print(hat)
                if hat == (1,0):
                    self.FX_right = 1
                    print("FX_right")
                if hat == (-1,0):
                    self.FX_left = 1
                    print("FX_left")
                if hat == (0,1):
                    self.FX_up = 1
                    print("FX_up")
                if hat == (0,-1):
                    self.FX_down = 1
                    print("FX_down")


            clock.tick(30)



##########################
# Test the Xbox class module.
xbox = XBOX_class()
xbox.initialize_xbox()
xbox.get_xbox_status()
print(xbox.done)
# Test End.
##########################