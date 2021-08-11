'''
Date: 2021-08-10 15:00:51
LastEditors: Guo Yuqin,12032421@mail.sustech.edu.cn
LastEditTime: 2021-08-11 10:47:13
FilePath: /servoDogVersion1.0/Xbox_value.py
'''

import pygame


# Initialize the pyname module
pygame.init()

# Initialize the joystick sub-module
pygame.joystick.init()

class X_Struct:
    
    def __int__(self):
        
        # TODO: Define the function of the axes & buttons of the XBOX controller
    
        # ID of the joystick
        self.joystick = None
        # There are 6 axes in the XBOX joystick controller
        self.axis_0 = 0.0
        self.axis_1 = 0.0
        self.axis_2 = -1.0
        self.axis_3 = 0.0
        self.axis_4 = 0.0
        self.axis_5 = -1.0

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


        # initialize the xbox joystick controller
        # return the flag of the 
        # self.joystick = self.initialize_xbox()


    def initialize_xbox(self):

        # initialize the clock block
        # clock = pygame.time.Clock()

        # Initialize the joystick No.1, can integrated with more than 1 joystick
        joystick_count = pygame.joystick.get_count()

        if joystick_count == 1:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            self.name = self.joystick.get_name()

            print("Joystick ID:",self.joystick)
            # print("The Name of the Joystick:",self.name)
            
        # Get the number of axes
        self.axes = self.joystick.get_numaxes()
        # print("number of axes:", self.axes)

        # Get the number of the buttons
        self.buttons = self.joystick.get_numbuttons()
        # print("number of buttons:",self.buttons)
        
        # Get the number of the hats
        self.hats = self.joystick.get_numhats()
        # print("number of hats:", self.hats)

        # print("Initialization is done!")
        # return self.joystick
        # print(self.joystick.get_power_level())


    def get_xbox_status(self):
        
        ## TODO: need to integrate with the non-class abjustment

        # # Get the status of the axes
        # for i in range( axes ):
        #     axis = joystick.get_axis( i )
        #     if i==1 and axis == -1.0:
        #         self.left_up = 1
        #     if i==1 and axis > 0.3:
        #         self.left_down = 1
        #     if i==0 and axis == -1:
        #         self.left_left = 1
        done = False
        clock = pygame.time.Clock()

        while done==False:
            
            # self.initialize_xbox()
            # EVENT PROCESSING STEP
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done=True # Flag that we are done so we exit this loop
                
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
                    print("Connect")


            for i in range( self.hats ):
                hat = self.joystick.get_hat( i )
                print(hat)
                if hat == (1,0):
                    self.FX_right = 1
                    print("FX_right:1")
                if hat == (-1,0):
                    self.FX_left = 1
                    print("FX_left:1")
                if hat == (0,1):
                    self.FX_up = 1
                    print("FX_up")
                if hat == (0,-1):
                    self.FX_down = 1
                    print("FX_down")


            clock.tick(10)



xbox = X_Struct()
xbox.initialize_xbox()
xbox.get_xbox_status()
    

