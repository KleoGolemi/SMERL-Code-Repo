import random
import numpy as np
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt
import math
import datetime
import csvwrite as csv
import multiprocessing as mp
import concurrent.futures
###############################################################################################################################
###############################################################################################################################
############################################### Dashboard #####################################################################

def constrain(number, lower_limit, upper_limit):
    return max(lower_limit, min(number, upper_limit))




# Define the robot class
class Robot:
    def __init__(self, ID, x, y, z, radius, velocity):
        self.ID = ID            ##identification ID
        self.x = x              ##x-coord
        self.y = y              ##y-coord
        self.z = z              ##z-coord
        self.radius = radius    ##size of bot
        self.speed = velocity         ##speed of bot [TODO: make this a variable]
        self.Fire = False       ##senses fire
        self.alive = True       ##is bot alive
        self.battery = 100      ##battery life
        self.neighbors = []     ##proxy neighbors [constantly will update]
        self.angle = random.uniform(0, 2*math.pi)   ##angle which the robot is facing


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
    def detectFire(self, measured_fire_coord):
        self.Fire = False                           ##this is intialized as false because when it was an else statement, it would occur last and make the result inaccurate
        for valuex in np.arange(self.radius*2):     ##the length will be the robot
            for valuey in np.arange(self.radius*2): ##the length of the robot
                y_coord = constrain(self.y - self.radius + valuey, 0, height-1) ##this will make sure that the robots only sense within the area [no out of bounds errors] 
                x_coord = constrain(self.x - self.radius + valuex, 0, width-1)  ##this will make sure that the robots only sense within the area [no out of bounds errors]
                if background_pixels[y_coord][x_coord][0] == 255:     ##if the red value is 255; this sensed the smoked portion and non-smoked portion
                    self.Fire = True    ##set robot class varibale to true
                    measured_fire_coord = add_reading(y_coord, x_coord, 1, measured_fire_coord)     ##this will add the vote of the drone to the approprite pixel location
                else:
                    measured_fire_coord = add_reading(y_coord, x_coord, -1, measured_fire_coord)     


    ##enviroment factor that may kill robot due to fire
    ##this is an instance of failure conditions
    def deadToFire(self):
        if background_pixels[self.y][self.x][0] == 255:        ##if the robot is directly over the fire
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
    def calculate_distance(self,ListofPositions):       ##pass in the list of robots with their location
        listIndex = []  ##store the distance of this robot from each other robot
        self_location = [self.x, self.y, self.z]
        for bot in ListofPositions:
            distance = euclidean(self_location, [bot[1], bot[2], bot[3]])
            listIndex.append([bot[0], distance])    ##robot ID and the distance from self
        return listIndex

def createRobots(num_robots, radius, velocity): 
    robots = [Robot(_, random.randint(2*radius, width - (2*radius)), random.randint(2*radius , height - (2*radius)), random.randint(-height, height), radius, velocity) for _ in range(num_robots)]
    return robots

##this is where the sensedMap is with the voting system
def add_reading(y,x, reading, addresses):       ##this function takes the coordinate and add it to a list where we can see what the consensus on that spot is 
    placeholder = addresses[y][x][2]
    placeholder.append(reading)
    addresses[y][x][2] = placeholder         ## make change

    return addresses

##TODO: This should be replaced with convert_vote below. This will cause the show output to change
def final_reading(addresses):           ##given the output of the add_reading, look at each array and sum the opinions 
    background_pixels = [[[255, 255, 255] for _ in range(width)] for _ in range(height)] ##undecided[white] by default
    for y, row in enumerate(addresses):
            for x,elem in enumerate(row):
                    if sum(elem[2]) > 0:     ##if sum > 0  [fire]
                        background_pixels[y][x] = [255,0,0]        
                    if sum(elem[2]) < 0:     ##if sum <0 [no fire]
                        background_pixels[y][x] = [0,0,0]
                    
    return addresses        ##for reference, if sum == 0 [undecided], if sum>0 [fire], if sum <0 [no fire]
##I return addresses yet the math is done on background_pixels[y][x]

##After the swarm sensing have voted on measured_fire_coord, this function will take those and convert it to RGB
def convert_vote(addresses):           ##given the output of the add_reading, look at each array and sum the opinions 
    background_pixels = [[[255, 255, 255] for _ in range(width)] for _ in range(height)] ##undecided[white] by default
    for x, row in enumerate(addresses):
            for y,elem in enumerate(row):
                    if sum(elem[2]) > 0:     ##if sum > 0  [fire]
                        background_pixels[x][y] = [255,0,0]
                    if sum(elem[2]) < 0:     ##if sum <0 [no fire]
                        background_pixels[x][y] = [0,0,0]
                    
    return background_pixels        ##for reference, if sum == 0 [undecided], if sum>0 [fire], if sum <0 [no fire]


##to randomly create fire I pick a random value of spot where fire can start and then give it a random area.
#for functional interations, we can make the how many spot to generate and the bounds larger
##this can also have multiple plays of how "fire" generates
def setup():
    num_spots = random.randint(1, 10)
    for firePix in np.arange(num_spots):    #picks how many centers TODO: let the user decide the amount of location
        y_coordFire = random.randint(30, height-30)    #y coord
        x_coordFire = random.randint(30, width-30)    #x coord
        left_bound = random.randint(1,40)       #area 
        right_bound = random.randint(1,40)      #area
        top_bound = random.randint(1,40)        #area
        bottom_bound = random.randint(1,40)     #area
        for yPix in np.arange(y_coordFire - left_bound, y_coordFire + right_bound):
            for xPix in np.arange(x_coordFire - bottom_bound, y_coordFire + top_bound):
                if xPix > 10 and xPix < width-10 and yPix > 10 and yPix < height-10:
                    background_pixels[yPix][xPix] = [255, 0, 0]                 ##change the color
        background_pixels[y_coordFire] [x_coordFire] = [255, 0 , 255]           ##gives the center of the fire a 255 on B ([0,0,255]), which signifies there is smoke. This is used for the smoke spreading
    np.save("InitialMap", background_pixels)    ##saves the initial map to be look at afterward
    initialMap = background_pixels              ##saves it as a run time variable as well
    return background_pixels, initialMap

def spread_fire(background_pixels):         ##this function is suppose to model fire spreading //this slows the simulation down significantly as well 
    for y in range(height):                 ##look at each pixel in the array
        for x in range(width):
            if background_pixels[y][x][0] == 255:        ##if its red
                for dy in [-1,0,1]:                         ##look at its neighbors
                    for dx in [-1,0,1]:
                        new_x, new_y = x + dx, y + dy
                        if 0 <= new_x <width and 0 <= new_y <height and background_pixels[new_y][new_x][0] !=255:   ##if its neighbors are not red and in bounds
                            if np.random.rand() < .01: ##spread probability  ##see if youre going to spread to it TODO: param
                                background_pixels[new_y][new_x] = [x + y for x, y in zip(background_pixels[new_y][new_x], [255,0, 0])]     ##if you are then make that pixel red
    return background_pixels


##Lets make smoke an event where picks to start somewhere within the fire, and it grows in all directions [can change to one direction]
# the smoke will be adding 255 to the blue.
#NOTE: Red ==  Fire no smoke [255,0,0], Pink == Smoke ontop of Fire [255,0,255], Blue == Smoke on nonfire [0,0,255]
def develope_smoke(background_pixels):
    for y in range(height):                 ##look at each pixel in the array
        for x in range(width):
            if background_pixels[y][x][2] == 255:        ##if its smoke 
                for dy in [-1,0,1]:                         ##look at its neighbors
                    for dx in [-1,0,1]:
                        new_x, new_y = x + dx, y + dy
                        if 0 <= new_x <width and 0 <= new_y <height and background_pixels[new_y][new_x][2] !=255:   ##if its neighbors are in  and not smoked yet
                            if np.random.rand() < .05: ##spread probability  ##see if youre going to spread to it TODO: param
                                background_pixels[new_y][new_x] = [x + y for x, y in zip(background_pixels[new_y][new_x], [0,0,255])]
    return background_pixels


#################################################OUTPUT READING#############################################################
def compareOutput(array1, array2):      ##what portion of the map is accurately detected [general map]
    correct = 0                         ##initiate 
    total = 0                           ##initiate
    for y in range(height):
        for x in range(width):
            value1 = list(array1[y][x]) ##note list is so I can compare the array as colors 
            value2 = list(array2[y][x]) ##note list is so I can compare the array as colors 
            if value1 == value2:
                correct += 1
            total += 1
    map_recreated = (correct/total) * 100
    return map_recreated

def detectAllFire(array1, array2):
    correct = 0                             ##reset each call
    total = 0                               ##reset each call
    for y in range(height):
        for x in range(width):
            if int(array1[y][x][0]) == 255:     ## for every red [255, x, x] cell in the background check if has been sensed
                value1 = int(array1[y][x][0])   ##output is is rgb color
                value2 = int(sum(array2[y][x][2]))  ##the output is in voting stage, so i have to do the conversion TODO: Fix such that what i pass in is in RGB
                if value1 == 255 and value2 >= 1:
                    correct += 1
                total += 1
    map_recreated = (correct/total) *100           ##if this is 100 [all the fire is detected] success condition
    return map_recreated



#############################################################################################################################
# Main game loop
def runSim(robots, background_pixels):
    running = True
    while running:
        robotLocation = []                      ##reset robot location array each run
    ######################################################################################################
        # Update and draw each robot
        # this will be the motion/robotics forloop
    ######################################################################################################    
        for robot in robots:
            robot.move()            ##robot movement 
            robot.detectFire(measured_fire_coord)      ##detect and record for fire in map
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
        measured_fire_coord_processed = final_reading(measured_fire_coord)      ##this should be where the voting becomes RGB
        ratio = detectAllFire(background_pixels, measured_fire_coord_processed) ##calculate the ratio each run [of fire detected]
        fireRatio.append(ratio)     ##update to update the plot on runtime
            
        #background_pixels = spread_fire(background_pixels)  ##NOTE: comment this to remove spread  
        #background_pixels = develope_smoke(background_pixels)  ##NOTE: comment this to remove spread
        ##if len(fireRatio) > 100:     ##time cutoff       TODO: Param
        if ratio > 95 or len(fireRatio) >1000:               ##if all the fire is sensed
            running = False
            np.save("ActualMap", background_pixels)     ##Actual map (only useful if there is spread)
            print("This is the amount of ticks it takes to detect all fire: ", len(fireRatio))  ##report how many ticks it took
            return len(fireRatio)
def execSim(numbots, radius, velocity):
    background_pixels, initialMap = setup()
    robots = createRobots(numbots, radius, velocity)
    output = runSim(robots, background_pixels)
    print(output)
    csv.csvwrite(filename, [numbots, radius, velocity, output])



# for num in [10,30]:
#     for size in [5,20]:
#         for velocity in [5, 10]:
#             frac_correct = [size, num, velocity]
#             for x in range(3):   

#                 fireRatio = []
#                 # Set up the screen dimensions
#                 width, height = 400, 200            ##TODO: size of the areana (pixels)[make variable] // optional [original is 800,600]
#                 ####background is filled black
#                 background_pixels = [[[0, 0, 0] for _ in range(width)] for _ in range(height)]
#                 # Global variables to store map awareness
#                 measured_fire_coord = [[[x,y, [0]] for y in range(width)] for x in range(height)] ##sensed area of all robots, includes vote
#                 initialMap = [] ##global variable of to store inital map


#                 ##Param
#                 radius = size
#                 numbots = num
#                 velocity = velocity
#                 execSim(numbots, radius, velocity)
#                 #     # Create a ThreadPoolExecutor
#                 with concurrent.futures.ProcessPoolExecutor() as executor:
#                 #     # Submit the tasks to the executor and map them to the values of i and j
#                     futures = [executor.submit(execSim, numbots, radius, velocity) for numbots in range[5, 30] for radius in [5,20] for velocity in [5,10]]

###########################GLOBAL VARIABLES##############################################

location = 'RobotSim\Data\TestRun'
current_datetime = datetime.datetime.now()    ##get the time for unique naming
current_day = str(current_datetime.strftime("%Y_%m_%d"))
current_time = str(current_datetime.strftime("%H_%M_%S"))
Param1 = '_numBots'
Param2 = '_area_'
#filename = location + Param1 + Param2 + current_day + current_time + '.csv'
filename = 'test.csv'
processes = []


fireRatio = []
width, height = 400, 200
background_pixels = [[[0, 0, 0] for _ in range(width)] for _ in range(height)]
measured_fire_coord = [[[x,y, [0]] for y in range(width)] for x in range(height)]
initialMap = []

##########################################################################################

if __name__ == '__main__':
    mp.freeze_support()
    with mp.Pool() as pool:
        for _ in range(3):          ##this makes it such that the it will do the 8 at a time, then start on the 3 runs of it
            results = [pool.apply_async(execSim, args=(numbots, radius, velocity)) for numbots in [10, 30] for radius in [5, 20] for velocity in [5, 10]]
            output = [result.get() for result in results]
        # Process the output as needed
## Possible smoke formula Probability of smoke detection = Sensitivity * Concentration * Distance * Ambient light level

####look into a more efficient way to update the screen instead of going to every pixel ##probably not feasable

## The CSV should prolly be [meta data] time,[config] num bots,[config] arena area,[config] velocity,[config] fire detection probability,[config] spread rate of fire, [config] spread rate of smoke, [output] frac_correct (% of map recreated)

##vary num robots and velocity and see how long is it makes for entire fire detection 

##TODO: work on a generating more interesting fires

##the data can be sorted through higlighting the box and pressing filter