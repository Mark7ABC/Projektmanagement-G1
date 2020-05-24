"""raspi controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Motor, Camera
from scipy.spatial import distance

TIME_STEP = 1064

# create the Robot instance.
robot = Robot()

MAX_SPEED = 6.28

cm = robot.getCamera('CAM')
cm.enable(TIME_STEP)


# get the motor devices
leftMotor = robot.getMotor('left wheel motor')
rightMotor = robot.getMotor('right wheel motor')
# set the target position of the motors
leftMotor.setPosition(10.0)
rightMotor.setPosition(10.0)

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

def find_robot():
    #Konstanten
    threshold = 10
    find_count = 3
    find_color = (72,19,56)
    
    image = cm.getImageArray()
    found = 0
    
    for x in range(0,cm.getWidth()):
        for y in range(0,cm.getHeight()):
            red   = image[x][y][0]
            green = image[x][y][1]
            blue  = image[x][y][2]
            
            img_color = (red,green,blue)
            
            d = distance.euclidean(img_color,find_color)
            
            if (d < threshold):
                #print ('r='+str(red)+' g='+str(green)+' b='+str(blue))
                found += 1
                if found >= find_count:
                    #print ('x='+str(x)+' y='+str(y))
                    return x
    

# set up the motor speeds at 10% of the MAX_SPEED.
#leftMotor.setVelocity(0.2 * MAX_SPEED)
#rightMotor.setVelocity(0.2 * MAX_SPEED)

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(TIME_STEP) != -1:
    x = find_robot()
    
    if x is None:
        #SearchModus --> Marker ist nicht auf Kamera Bild
        continue
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
        
        leftMotor.setVelocity(left_vel * MAX_SPEED)
        rightMotor.setVelocity(right_vel * MAX_SPEED)
        
    
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    pass

# Enter here exit cleanup code.
