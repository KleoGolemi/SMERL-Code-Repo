import pygame
import random
import numpy as np
#import UI           ##this will import the IU for the varibales to be inputted
##import streamlitDash
##from streamlitDash import startFlag
#from UI import var1_result, var2_result, var3_result, distribution_result, EnterBox     ##this are the variable values I will import from the sliders
from scipy.spatial.distance import euclidean
import streamlit as st
import matplotlib.pyplot as plt
import math
###############################################################################################################################
###############################################################################################################################
############################################### Dashboard #####################################################################

# Global variables to store slider values
global_slider1_value = None
global_slider2_value = None

def constrain(number, lower_limit, upper_limit):
    return max(lower_limit, min(number, upper_limit))

# Set up the layout using columns
col1, col2, col4 = st.columns([50,25,25])
col3, col5, col6 = st.columns([50,25,25])

# Section 1: Sliders
with col1:
    st.header("Param Change")
    slider1_value = st.slider("Number of Robots", 0.0, 50.0, 25.0, step = 1.0)
    slider2_value = st.slider("Robot Velocity", 0.0, 20.0, 10.0, step = 1.0)
    slider3_value = st.slider("Sensor Accuracy", 0.0, 1.0, .95)
    slider4_value = st.slider("Sensor Range", 0.0, 1.0, .5)
    slider5_value = st.slider("Robot Battery (in terms of mission length)", 0.0, 1.0, (.5, .8))
    slider6_value = st.slider("Fill Ratio", 0.0, 1.0, .5)
    slider7_value = st.slider("Mission Length (Ticks)", 1.0, 1000.0, 500.0, step= 1.0)

# Section 2: Drop-downs
with col2:
    st.header("Mission Selection")
    option0 = st.selectbox("Mission Objective", ["Mission A" , "Mission B" , "Mission C"])
    option1 = st.selectbox("Phase", ["Option A", "Option B", "Option C"])
    option2 = st.selectbox("Swarm Baseline [Consensus]", ["Option X", "Option Y", "Option Z"])
    option3 = st.selectbox("SWARM Baseline [Motion]", ["Option Alpha", "Option Beta", "Option Kappa"])
    option4 = st.selectbox("Communication Baseline [Routing Protocol]", ["Option 1", "Option 2", "Option 3"])

# Section 4: Text
with col4:
    st.header("Mission Summary")
    st.write("Mission:", option0)
    st.write("Phase:", option1)
    st.write("Swarm Baseline:", option2)
    st.write("Communication Baseline:", option3)
    calculate_button = st.button("Calculate")


# Function to update the plots
def update_plots_realtime(fireRatio):

    ##here I can bring the data back
    # Generate data based on global slider values
    x1 = np.arange(len(fireRatio))
    y1 = fireRatio

    # Create the first plot
    fig1, ax1 = plt.subplots()
    ax1.plot(x1, y1)
    ax1.set_xlabel("X")
    ax1.set_ylabel("Y1")

    # Update the plots in the Streamlit app
    plot1_placeholder.pyplot(fig1)

    # Pause to allow time for slider updates
    # st.pause(0.1)
    plt.close(fig1)

# Check if calculate button is clicked
if calculate_button:
    # Store slider values in global variables
    startFlag = 424
    global_slider1_value = slider1_value
    global_slider2_value = slider2_value

# Section 3: Output Plots
    with col3:
        st.header("Output Plots")
        plot1_placeholder = st.empty()
    with col5:
        st.header("MOPs")
        st.write("Winner Winner Chicken Dinner")
    with col6:
        st.header("MOEs")
        st.write("Winner Winner Chicken Dinner")    

        # Clear the file
    with open('output.txt', 'w') as file:
        pass


    # Create a list of strings
    data = [startFlag, global_slider1_value, global_slider2_value]

    # Write the list to the file
    np.savetxt('output.txt', data, fmt='%s')


    #######################################################
    ##here i pass it to the sim and get a response



    #######################################################

    # Start updating the plots
    #update_plots = True
    #update_plots_realtime()     ##feed the information here

#####################################################################################################################################
#####################################################################################################################################
############################################### Dashboard End #######################################################################

loadedData = np.loadtxt('C:/Users/pando/.vscode/PythonCode/FunScripts/RobotSim/output.txt')
flag = loadedData[0]
fireRatio = []


##print(f"this is the Sim.py file with varibales from UI {var1_result}, and {var2_result}")
if flag == 424:


    with open('output.txt', 'w') as file:
        pass

    startFlag = 000

    # Create a list of strings
    data = [startFlag, global_slider1_value, global_slider2_value]


    ##Param
    radius = 10

    # Write the list to the file
    np.savetxt('output.txt', data, fmt='%s')



    # Initialize Pygame
    pygame.init()                 ##NOTE: Add this back 

    # Set up the screen dimensions
    width, height = 400, 200            ##TODO: size of the areana (pixels)[make variable] // optional [original is 800,600]
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    ####background is filled black
    background_pixels = [[[0, 0, 0] for _ in range(width)] for _ in range(height)]
    # Create a swarm of robots
    # Define the colors
    BLACK = [0, 0, 0]
    WHITE = [255, 255, 255]
    sin45 = np.sqrt(2)/2
    # Global variables to store map awareness
    measured_fire_coord = [[(x,y, list([0])) for y in range(width)] for x in range(height)] ##possibly change the x&y
    comaper2 = measured_fire_coord



    # Define the robot class
    class Robot:
        def __init__(self, ID, x, y, z, radius):
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
            
        ##this variable updates the visulas and is called repeatedly
        def draw(self):      
            if self.alive == True:          
                color_value = abs(self.z)  # Calculate color based on absolute value of z
                color = (0, color_value % 256, 255 - color_value % 256)  # Blue to red gradient based on absolute value of z [height parameter]
                pygame.draw.circle(screen, color, (self.x, self.y), self.radius)    ##draws bot
                font = pygame.font.Font(None, 20)
                text = font.render("Fire Reading:"  + " " + str(self.Fire) + " ID#: " + str(self.ID), True, WHITE) ##text output per bot
                text_rect = text.get_rect(center=(self.x, self.y - 20))
                screen.blit(text, text_rect)



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
        robots = [Robot(_, random.randint(2*radius, width - (2*radius)), random.randint(2*radius , height - (2*radius)), random.randint(-height, height), radius) for _ in range(num_robots)]
        return robots

    def fireDetected(robots):
        robotswFire = [robot for robot in robots if robot.Fire == True]
        ratio = len(robotswFire)/len(robots)
        return ratio

    def add_reading(y,x, reading, addresses):       ##this function takes the coordinate and add it to a list where we can see what the consensus on that spot is 

        array_tobe = list(addresses[y][x][2])       ##datatype manipulation because tuple cannot be changed
        array_tobe.append(reading)                  ##append to list 
        addresses[y][x] = list(addresses[y][x])  # Convert tuple to list
        addresses[y][x][2] = array_tobe         ## make change
        addresses[y][x] = tuple(addresses[y][x])  # Convert back to tuple

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
        np.save("InitialMap", background_pixels)
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
    

    # Quit the program
    def quitSim():
        pygame.quit()
#################################################OUTPUT READING#############################################################
    def show_output_setup(measured_fire_coord):         ##this will show what the robots picked up
        pygame.init()                 ##NOTE: Add this back 

    # Set up the screen dimensions
##        width, height = 800, 600            ##TODO: size of the areana (pixels)[make variable] // optional 
        screen = pygame.display.set_mode((width, height))
        background_pixels = [[[255, 255, 255] for _ in range(width)] for _ in range(height)] ##undecided[white] by default
        for row in measured_fire_coord:
            for elem in row:
                if elem[2] > 0:     ##if sum > 0  [fire]
                    background_pixels[elem[0]][elem[1]] = [255,0,0]
                if elem[2] < 0:     ##if sum <0 [no fire]
                    background_pixels[elem[0]][elem[1]] = [0,0,0]
        np.save("SensedMap", background_pixels)

        frac_correct = compareOutput(np.load('ActualMap.npy'), np.load('SensedMap.npy'))
        fire_found = detectAllFire(np.load('ActualMap.npy'), np.load('SensedMap.npy'))
        print(frac_correct)
        print(fire_found)

        print(len(background_pixels))
        print(len(background_pixels[0]))
        print(len(background_pixels[0][0]))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            for y in range(height):
                for x in range(width):
                    pygame.draw.rect(screen, background_pixels[y][x], (x, y, 1, 1)) ##draw it
            pygame.display.flip()

    def compareOutput(array1, array2):      ##what portion of the map is accurately detected
        correct = 0
        total = 0
        for y in range(height):
            for x in range(width):
                value1 = list(array1[y][x]) ##note list is so I can compare the array 
                value2 = list(array2[y][x])
                my_list = value1 == value2
                if my_list:
                    correct += 1
                total += 1
        map_recreated = (correct/total) * 100
        return map_recreated
    
    def detectAllFire(array1, array2):
        correct = 0
        total = 0
        for y in range(height):
            for x in range(width):
                if int(array1[y][x][2]) == 255:     ## if the cell we are looking at is red
                    #print("Got here")
                    value1 = int(array1[y][x][2]) ##note list is so I can compare the array 
                    value2 = int(array2[y][x][2])   ##TODO: this is always 0,0,0. Look into why, maybe the file i gave it isnt loading right
                    #print(value1)
                    #print(value2)
                    my_list = value1 == value2
                    if my_list:
                        correct += 1
                    total += 1
        map_recreated = (correct/total) *100           ##if this is 1 all the fire is detected
        return map_recreated
    


#############################################################################################################################
    # Main game loop
    def runSim(robots, background_pixels):
        running = True
        while running:
            robotLocation = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Draw each pixel on the screen(because I am filling every pixel individually it takes a while)
            for y in range(height):
                for x in range(width):
                    pygame.draw.rect(screen, background_pixels[y][x], (x, y, 1, 1))
        ######################################################################################################
            # Update and draw each robot
            # this will be the motion/robotics forloop
        ######################################################################################################    
            for robot in robots:
                robot.move()            ##robot movement 
                robot.detectFire(measured_fire_coord)      ##checks for fire
                robot.draw()            ##update visuals 
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
            #np.save("SensedMap", background_pixels)
            #ratio = detectAllFire(np.load('ActualMap.npy'), np.load('SensedMap.npy'))
            print(ratio)
            fireRatio.append(ratio)
            #print(ratio)
            update_plots_realtime(fireRatio)
                
            #print(robotLocation)
            pygame.display.flip()
            #background_pixels = spread_fire(background_pixels)  ##NOTE: comment this to remove spread  
            #background_pixels = develope_smoke(background_pixels)  ##NOTE: comment this to remove spread
            clock.tick(10)
            ##if len(fireRatio) > 100:     ##time cutoff       TODO: Param
            if len(fireRatio) == 50:  
                running = False
                np.save("ActualMap", background_pixels)     ##Actual map (only useful if there is spread)
                #print(len(fireRatio))
                quitSim()


    background_pixels = setup()
    robots = createRobots(int(loadedData[1]))
    runSim(robots, background_pixels)
    print("Code works")
    measured_fire_coord = final_reading(measured_fire_coord)
    #print(measured_fire_coord)
    show_output_setup(measured_fire_coord) ##this works, it will just need more fine tuning
 

    ##TODO: Look into the fire that doesnt grow if its 1 pixel large
    ## Possible smoke formula Probability of smoke detection = Sensitivity * Concentration * Distance * Ambient light level
    ####look into a more efficient way to update the screen instead of going to every pixel ##probably not feasable

    ## The CSV should prolly be [meta data] time,[config] num bots,[config] arena area,[config] velocity,[config] fire detection probability,[config] spread rate of fire, [config] spread rate of smoke, [output] frac_correct (% of map recreated)

    ##vary num robots and velocity and see how long is it makes for entire fire detection 