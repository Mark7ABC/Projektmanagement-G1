"""raspi controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Motor, Camera
from scipy.spatial import distance

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
    
    def __init__(self):
        self.cm.enable(TIME_STEP)
        self.leftMotor.setPosition(float('inf'))
        self.rightMotor.setPosition(float('inf'))
        self.leftMotor.setVelocity(0.0)
        self.rightMotor.setVelocity(0.0)
    
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
        
class EscapeMode:
    def loopFunction(self,controller):
        print('nothinghappens')

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
                        
    def loopFunction(self, controller):
        x = self.find_robot(controller.TrackingColor)
        
        if x is None:
            #SearchModus --> Marker ist nicht auf Kamera Bild
            print('None')
        else:
            left_vel = 0.1
            right_vel = 0.1
        
            if (48 < x <= 64):
               left_vel += 0.05
            elif (32 < x <= 48):
                left_vel += 0.025
            elif (16 < x < 32):
                right_vel += 0.025
            elif (0 < x <= 16):
               right_vel += 0.05
            
            controller.setVelocity_leftMotor(right_vel)
            controller.setVelocity_rightMotor(left_vel)
    

# set up the motor speeds at 10% of the MAX_SPEED.
#leftMotor.setVelocity(0.2 * MAX_SPEED)
#rightMotor.setVelocity(0.2 * MAX_SPEED)

controller = MainController()
pMode = PursuerMode()
eMode = EscapeMode()

# Main loop:
while robot.step(TIME_STEP) != -1:
    
    if (controller.OpMode == 0):
        pMode.loopFunction(controller)
    elif (controller.OpMode == 1):
        eMode.loopFunction(controller)
   

    pass

# Enter here exit cleanup code.
