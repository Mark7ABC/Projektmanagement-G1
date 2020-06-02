"""raspi controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Motor, Camera, LED, DistanceSensor
from scipy.spatial import distance
import time, sys

TIME_STEP = 64

robot = Robot()
timestep = int(robot.getBasicTimeStep())



class MainController:
    MAX_SPEED = 6.28
    cm = robot.getCamera('CAM')
    leftMotor = robot.getMotor('left wheel motor')
    rightMotor = robot.getMotor('right wheel motor')
    OpMode = 0
    TrackingColor = (72,19,56)
    led = robot.getLED('stateled')
    dsensor = robot.getDistanceSensor('distance sensor')
    
    def __init__(self):
        self.cm.enable(TIME_STEP)
        self.leftMotor.setPosition(float('inf'))
        self.rightMotor.setPosition(float('inf'))
        self.leftMotor.setVelocity(0.0)
        self.rightMotor.setVelocity(0.0)
        self.dsensor.enable(TIME_STEP)
        
        if self.OpMode == 1:
            self.led.set(0x0000FF)
        elif self.OpMode == 0:
            self.led.set(0xFF0000)
    
    def setVelocity_leftMotor(self, vel):
        self.leftMotor.setVelocity(vel * self.MAX_SPEED)
    
    def setVelocity_rightMotor(self, vel):
        self.rightMotor.setVelocity(vel * self.MAX_SPEED)
    
    def getImageArray(self):
        return self.cm.getImageArray()
    
    def getImageWidth(self):
        return self.cm.getWidth()
        
    def getImageHeight(self):
        return self.cm.getHeight()
    
    def SetLEDColor(self, color):
        self.led.set(color)
    
    def getUSonicSensor(self):
        val = self.dsensor.getValue()
        return val
    
    def Wait1Second(self):
        robot.step(1000)
    
    def getFloorSensor(self):
        val = 0
        return val
        
        
class EscapeMode:
    def loopFunction(self,controller):
        print('nothinghappens')
    def StartupFunction(self,controller):
        controller.SetLEDColor(0x00FF00)
        #10sek warten bis Rundenbeginn
        for i in range(1,10):
            controller.Wait1Second()
            print(str(10-i) + ' Sekunden bis zum Start')
    
class PursuerMode:
    def find_robot(self, tColor):
        #Konstanten
        threshold = 10
        find_count = 3

        image = controller.getImageArray()
        found = 0
        
        for x in range(0,controller.getImageWidth()):
            for y in range(0,controller.getImageHeight()):
                red   = image[x][y][0]
                green = image[x][y][1]
                blue  = image[x][y][2]
                
                img_color = (red,green,blue)
                
                d = distance.euclidean(img_color, tColor)
                
                if (d < threshold):
                    #print ('r='+str(red)+' g='+str(green)+' b='+str(blue))
                    found += 1
                    if (found >= find_count):
                        #print ('x='+str(x)+' y='+str(y))
                        return x
    
    def StartupFunction(self, controller):
        controller.SetLEDColor(0x00FF00)
        #10sek warten bis Rundenbeginn
        for i in range(1,11):
            controller.Wait1Second()
            print(str(10-i) + ' Sekunden bis zum Start')
        
        #3sek warten weil Fängermodus
        for i in range(1,4):
            controller.Wait1Second()
            print('Fängermodus in ' + str(3-i) + ' Sekunden aktiv!')
        
                        
    def loopFunction(self, controller):
        x = self.find_robot(controller.TrackingColor)
        
        #left = 1;right = 0
        left_or_right = 1
        if controller.getUSonicSensor() > 300.0:
            if x is None:
                #SearchModus --> Marker ist nicht auf Kamera Bild
                left_vel = -0.4
                right_vel = 0.4
                invert = 1
                
                if left_or_right == 0:
                    invert = -1
                
                controller.setVelocity_leftMotor(invert * right_vel)
                controller.setVelocity_rightMotor(invert * left_vel)
            else:
                left_vel = 0.4
                right_vel = 0.4
            
                if (48 < x <= 64):
                   left_vel += 0.05
                   left_or_right = 0
                elif (32 < x <= 48):
                    left_vel += 0.025
                    left_or_right = 0
                elif (16 < x < 32):
                    right_vel += 0.025
                    left_or_right = 1
                elif (0 < x <= 16):
                   right_vel += 0.05
                   left_or_right = 1
                
                controller.setVelocity_leftMotor(right_vel)
                controller.setVelocity_rightMotor(left_vel)
        else:
            print('Gegnerische Roboter wurde gefangen!')
            controller.setVelocity_leftMotor(0.0)
            controller.setVelocity_rightMotor(0.0)
            sys.exit()
    
controller = MainController()
pMode = PursuerMode()
eMode = EscapeMode()

start_function_run = 0

# Main loop:
while robot.step(TIME_STEP) != -1:

    if (controller.OpMode == 0):        
        if start_function_run == 0:
            start_function_run = 1
            pMode.StartupFunction(controller)
        
        pMode.loopFunction(controller)
        
    elif (controller.OpMode == 1):
        if start_function_run == 0:
            start_function_run = 1
            eMode.StartupFunction(controller)
        
        eMode.loopFunction(controller)
        
    pass

# Enter here exit cleanup code.
