import random
import numpy as np
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt
import math
import csvwrite as csv
import datetime
###############################################################################################################################
###############################################################################################################################
############################################### Dashboard #####################################################################


def constrain(number, lower_limit, upper_limit):
    return max(lower_limit, min(number, upper_limit))


# Define the robot class
class Robot:
    def __init__(self, ID, x, y, z):
        self.ID = ID            ##identification ID
        self.x = x              ##x-coord
        self.y = y              ##y-coord
        self.z = z              ##z-coord
        self.radius = radius        ##size of bot
        self.speed = 5         ##speed of bot [TODO: make this a variable]
        self.Fire = False       ##senses fire
        self.alive = True       ##is bot alive
        self.battery = 100      ##battery life
        self.neighbors = []     ##proxy neighbors [constantly will update]
        self.angle = random.uniform(0, 2*math.pi)


    ##this is the function responsible for moving the robots.
    ##within this function, there can be multiple 'plays' on how the robot should move
    ##the one below is a simple random motion 
    def move(self):
        if self.alive == True:
#########################MOTION OPTION 1############################################################################            
        # Randomly update the robot's position
        #    self.x += random.randint(-self.speed, self.speed)
        #    self.y += random.randint(-self.speed, self.speed)
        #    self.z += random.randint(-self.speed, self.speed)

            # Ensure the robot stays within the screen boundaries
        #    self.x = max(self.radius, min(self.x, width - self.radius))
        #    self.y = max(self.radius, min(self.y, height - self.radius))
######################################################################################################################

######################MOTION OPTION 2#################################################################################
            dx = self.speed * math.cos(self.angle)      ##given the angle you want to move, find the X
            dy = self.speed * math.sin(self.angle)      ##find the Y
            
            if self.x + dx - self.radius < 0 or self.x + dx + self.radius > width or self.y + dy - self.radius < 0 or self.y + dy +self.radius > height:
                self.angle = random.uniform(0, 2*math.pi) ##if your movement would cause anu part of you to be out of bounds, chage direction
            else:    ##otherwise make that movement, this is done to not have an error with checking for fire on unsupported pixels
                self.x += int(dx)
                self.y += int(dy)
##########################################################################################################################
    ##this function sees if the hitbox of the robot is touching a red pixel in the background.
    ##if it is. We then change the status of the internal Fire field within the Robot class which is then displayed with the draw function
    ##The out-of-bound scenario is tended to.
    # Note the hitbox is slightly bigger (a square) to make the code neater 
    ##this function also adds to the global array to recreate the map.
    ##The old function would only ping the center and corners, this will do the the entire area.
    def detectFire(self, measured_fire_coord):
        self.Fire = False                           ##this is intialized as false because when it was an else statement, it would occur last and make the result inaccurate
        for valuex in np.arange(self.radius*2):
            for valuey in np.arange(self.radius*2):
                y_coord = constrain(self.y - self.radius + valuey, 0, height-1)
                x_coord = constrain(self.x - self.radius + valuex, 0, width-1)
                if background_pixels[y_coord][x_coord][0] == 255:       ##TODO: change this to make it look at the color rather than just the red value. Formula it later
                    self.Fire = True
                    measured_fire_coord = add_reading(y_coord, x_coord, 1, measured_fire_coord)
                else:
                    measured_fire_coord = add_reading(y_coord, x_coord, -1, measured_fire_coord) ##TODO: make this an area       
    """    ##This is old way, this should only be used to know if the bot is ontop of fire. The other one does both fire detection, and sensing
        for valuex in np.arange(4):                 ##1,0,-1,0 sequence
            for valuey in np.arange(4):             ##1,0,-1,0 sequence
                x_coord = (self.x + int(np.cos(np.pi*valuex/2)*self.radius))%width
                y_coord = (self.y + int(np.cos(np.pi*valuey/2)*self.radius))%height
                if background_pixels[y_coord][x_coord] == (255,0,0): ##check if the pixel behind it is red. taking % to stay within the range.
                    ##make a distribution for its sensing probability. TODO: parameter from the UI which will decide the spread and cuttoff
                    ##if it is a value set it to true. 
                    self.Fire = True
                    measured_fire_coord = add_reading(y_coord, x_coord, 1, measured_fire_coord) ##TODO: make the an area
                else:
                    measured_fire_coord = add_reading(y_coord, x_coord, -1, measured_fire_coord) ##TODO: make this an area
    """



    ##enviroment factor that may kill robot due to fire
    ##this is an instance of failure conditions
    def deadToFire(self):
        if background_pixels[self.y][self.x] == [255, 0, 0]:        ##if the robot is directly over the fire
            ##apply distribution of robot dying                     TODO: have the user pick the distribution and cutoff
            ##if it is the right value, kill robot
            self.alive = False
        

    ##function to represent the batteries life of the robot  
    # Idea: We can make this function take a value, then it can be called within other functions to represent 
    # that different tasks can take different amount of battery to operate  
    def deadToBattery(self):
        if self.alive == True:
            self.battery = self.battery - .01           ##TODO: have the user decide on the value 
            self.alive = False


    ##this helper function will calculate the 3D distance from the robot calling the function to all other robots
    def calculate_distance(self,ListofPositions):
        listIndex = []
        self_location = [self.x, self.y, self.z]
        for bot in ListofPositions:
            distance = euclidean(self_location, [bot[1], bot[2], bot[3]])
            listIndex.append([bot[0], distance])
        return listIndex

def createRobots(num_robots):
    #num_robots = 20         ##TODO: Take this a variable 
    robots = [Robot(_, random.randint(2*radius, width-(2*radius)), random.randint(2*radius, height - (2*radius)), random.randint(-height, height)) for _ in range(num_robots)]
    return robots

def fireDetected(robots):
    robotswFire = [robot for robot in robots if robot.Fire == True]
    ratio = len(robotswFire)/len(robots)
    return ratio

def add_reading(x,y, reading, addresses):       ##this function takes the coordinate and add it to a list where we can see what the consensus on that spot is 

    array_tobe = list(addresses[x][y][2])       ##datatype manipulation because tuple cannot be changed
    array_tobe.append(reading)                  ##append to list 
    addresses[x][y] = list(addresses[x][y])  # Convert tuple to list
    addresses[x][y][2] = array_tobe         ## make change
    addresses[x][y] = tuple(addresses[x][y])  # Convert back to tuple

    return addresses

def final_reading(addresses):           ##given the output of the add_reading, look at each array and sum the opinions 
    ##tobo = 0
    for x, row in enumerate(addresses):
            for y,elem in enumerate(row):
                    tobo = sum(elem[2])
                    elem = list(elem)
                    elem[2] = tobo
                    elem = tuple(elem)
                    addresses[x][y] = elem
                    
    return addresses        ##for reference, if sum == 0 [undecided], if sum>0 [fire], if sum <0 [no fire]

def setup():

    ##to randomly create fire I pick a random value of spot where fire can start and then give it a random area.
    #for functional interations, we can make the how many spot to generate and the bounds larger
    ##this can also have multiple plays of how "fire" generates
    for firePix in np.arange(random.randint(1, 10)):    #picks how many centers TODO: let the user decide the amount of location
        y_coordFire = random.randint(1, height-1)    #y coord
        x_coordFire = random.randint(1, width-1)    #x coord
        left_bound = random.randint(1,40)       #area 
        right_bound = random.randint(1,40)      #area
        top_bound = random.randint(1,40)        #area
        bottom_bound = random.randint(1,40)     #area
        for yPix in np.arange(y_coordFire - left_bound, y_coordFire + right_bound):
            for xPix in np.arange(x_coordFire - bottom_bound, y_coordFire + top_bound):
                if xPix > 0 and xPix < width and yPix > 0 and yPix < height:
                    background_pixels[yPix][xPix] = [255, 0, 0]                 ##change the color
    #    for yPix in np.arange(height-200, height-1):                            ##this is for testing purposes
    #        for xPix in np.arange(width-200, width-1):
    #            if xPix > 0 and xPix < width and yPix > 0 and yPix < height:
    #                background_pixels[yPix][xPix] = (255, 0, 0)                 ##change the color
    #print(background_pixels)
    #print(len(background_pixels))
        background_pixels[y_coordFire] [x_coordFire] = [255, 0 , 255]
    return background_pixels

def spread_fire(background_pixels):         ##this function is suppose to model fire spreading //this slows the simulation down significantly as well 
    for y in range(height):                 ##look at each pixel in the array
        for x in range(width):
            if background_pixels[y][x] == [255,0,0] or  background_pixels[y][x] == [255,0,255]:        ##if its red
                for dy in [-1,0,1]:                         ##look at its neighbors
                    for dx in [-1,0,1]:
                        new_x, new_y = x + dx, y + dy
                        if 0 <= new_x <width and 0 <= new_y <height and background_pixels[new_y][new_x][0] !=255:   ##if its neighbors are not red and in bounds
                            if np.random.rand() < .01: ##spread probability  ##see if youre going to spread to it TODO: param
                                background_pixels[new_y][new_x] = [x + y for x, y in zip(background_pixels[new_y][new_x], [255,0, 0])]     ##if you are then make that pixel red
    return background_pixels


##Lets make smoke an event where picks to start somewhere within the fire, and it grows in all directions [can change to one direction]
# the smoke will be adding 155 to the blue. NOTE: this will break fire detection for the moment (it is simplified to only looking at the red value)
#NOTE: Red ==  Fire, Pink == Smoke ontop of Fire, Blue == Smoke on nonfire 
def develope_smoke(background_pixels):
    for y in range(height):                 ##look at each pixel in the array
        for x in range(width):
            if background_pixels[y][x] == [255,0,255] or background_pixels[y][x] == [0,0,255]:        ##if its smoke 
                for dy in [-1,0,1]:                         ##look at its neighbors
                    for dx in [-1,0,1]:
                        new_x, new_y = x + dx, y + dy
                        if 0 <= new_x <width and 0 <= new_y <height and background_pixels[new_y][new_x][2] !=255:   ##if its neighbors are in  and not smoked yet
                            if np.random.rand() < .05: ##spread probability  ##see if youre going to spread to it TODO: param
                                background_pixels[new_y][new_x] = [x + y for x, y in zip(background_pixels[new_y][new_x], [0,0,255])]
    return background_pixels


#################################################OUTPUT READING#############################################################
def show_output_setup(measured_fire_coord):         ##this will show what the robots picked up
    background_pixels = [[[255, 255, 255] for _ in range(width)] for _ in range(height)] ##undecided[white] by default
    for row in measured_fire_coord:
        for elem in row:
            if elem[2] > 0:     ##if sum > 0  [fire]
                background_pixels[elem[0]][elem[1]] = [255,0,0]
            if elem[2] < 0:     ##if sum <0 [no fire]
                background_pixels[elem[0]][elem[1]] = [0,0,0]
    np.save("SensedMap", background_pixels)

    frac_correct = compareOutput(np.load('ActualMap.npy'), np.load('SensedMap.npy'))
    print(frac_correct)
    return frac_correct

def compareOutput(array1, array2):      ##what portion of the map is accurately detected
    correct = 0
    total = 0
    for y in range(height):
        for x in range(width):
            value1 = list(array1[y][x])
            value2 = list(array2[y][x])
            my_list = value1 == value2
            if my_list:
                correct += 1
            total += 1
    map_recreated = (correct/total) * 100
    return map_recreated


#############################################################################################################################
# Main game loop
def runSim(robots, background_pixels):
    running = True
    while running:
        robotLocation = []
    ######################################################################################################
        # Update and draw each robot
        # this will be the motion/robotics forloop
    ######################################################################################################    
        for robot in robots:
            robot.move()            ##robot movement 
            robot.detectFire(measured_fire_coord)      ##checks for fire
            robotLocation.append([robot.ID, robot.x, robot.y, robot.z])    ##this will make a list of  which robots location

    ##########################################################################################################    
        ##calculate the distance is robot is from eachother
        ##this will be the "communication" for loop
    ##########################################################################################################
        for item in robots:
            directory = item.calculate_distance(robotLocation)      ##calculate the distance
            item.neighbors = [x for x in directory if x[1] < 50 and x[0] != item.ID]   ##update the robot class
            #print(f" Bots {item.ID} near neighbors are {nearNeighbor}")

    ##########################################################################################################
        ##here is the main [this is gods-eye, not getting the info from robots, i can access anything]
        ##functions which the swarm will report back 
    ##########################################################################################################
        ratio = fireDetected(robots) 
        fireRatio.append(ratio)
        background_pixels = spread_fire(background_pixels)  ##NOTE: comment this to remove spread  
        background_pixels = develope_smoke(background_pixels)  
        if len(fireRatio) > 100:     ##time cutoff       TODO: Param
            running = False
            np.save("ActualMap", background_pixels)


location = 'RobotSim\Data\TestRun'
current_datetime = datetime.datetime.now()    ##get the time for unique naming
current_day = str(current_datetime.strftime("%Y_%m_%d"))
current_time = str(current_datetime.strftime("%H_%M_%S"))
Param1 = '_numBots'
Param2 = '_area_'
filename = location + Param1 + Param2 + current_day + current_time + '.csv'
csv.csvwrite(filename, '')        ##reset csv to empty
for size in [5, 10, 20]:
    for num in [10,25]:         ##thid forloop will vary param1
        csv.csvwrite(filename, 'This is:' + str(size) + str(num))        ##reset csv to empty
        frac_correct = []
        for x in range(3):      ##this loop will be how many one config will run
            ##setup- re-instate variables
            ##User Defined
            num_bots = num              ##param1
            radius = size                 ##param2
            # Set up the screen dimensions
            width, height = 400, 200            ##TODO: size of the areana (pixels)[make variable] // optional [original is 800,600]
            fireRatio = [size, num]


            ####background is filled black
            background_pixels = [[[0, 0, 0] for _ in range(width)] for _ in range(height)]
            # Create a swarm of robots
            # Define the colors
            BLACK = [0, 0, 0]
            WHITE = [255, 255, 255]
            # Global variables to store map awareness
            measured_fire_coord = [[(x,y, list([0])) for y in range(width)] for x in range(height)] ##possibly change the x&y

            background_pixels = setup()
            robots = createRobots(num_bots)
            runSim(robots, background_pixels)
            print("Code works")
            measured_fire_coord = final_reading(measured_fire_coord)
            results = show_output_setup(measured_fire_coord) ##this works, it will just need more fine tuning
            frac_correct.append(results)
        print(frac_correct)
        csv.csvwrite(filename, frac_correct)


##TODO: Look into the fire that doesnt grow if its 1 pixel large
## Possible smoke formula Probability of smoke detection = Sensitivity * Concentration * Distance * Ambient light level
####look into a more efficient way to update the screen instead of going to every pixel ##probably not feasable

## The CSV should prolly be [meta data] time,[config] num bots,[config] arena area,[config] velocity,[config] fire detection probability,[config] spread rate of fire, [config] spread rate of smoke, [output] frac_correct (% of map recreated)