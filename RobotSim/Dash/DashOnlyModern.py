import random
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from sympy import symbols, Eq, solve

###############################################################################################################################
###############################################################################################################################
############################################### Dashboard #####################################################################

# Global variables to store slider values
startFlag = 000
global_slider1_value = None
global_slider2_value = None

# Set up the layout using columns (https://docs.streamlit.io/library/api-reference/layout/st.columns)
col1, col2, col4 = st.columns([50,50,25])
col3, col5, col6 = st.columns([50,50,25])

# Section 1: Sliders (Left most column) https://docs.streamlit.io/library/api-reference/widgets/st.slider
with col1:
    st.header("Param Change")
    slider1_value = st.slider("Number of Robots", 0.0, 50.0, 25.0, step = 1.0) # Format is st.slider(label, min, max, default, step)
    slider2_value = st.slider("Robot Velocity", 0.0, 20.0, 10.0, step = 1.0)
    slider3_value = st.slider("Sensor Accuracy", 0.0, 1.0, .95)
    slider4_value = st.slider("Communication Range", 0.0, 1.0, .5)
    slider5_value = st.slider("Fill Ratio", 0.0, 1.0, .5)
    slider6_value = st.slider("Mission Length (Ticks)", 1.0, 1000.0, 500.0, step= 1.0)

# Section 2: Drop-downs (Middle column) https://docs.streamlit.io/library/api-reference/widgets/st.selectbox
with col2:
    st.header("Mission Selection")
    option0 = st.selectbox("Mission Objective", ["Fire Detection" , "Mission B" , "Mission C"]) # Format is st.selectbox(label, [options array])
    st.write("The objective of the mission.")                  # Description of the drop-down             
    if option0 == "Fire Detection":                             # Conditional statement based on the drop-down value (only for Fire Detection mission at the moment)
        threshold = st.slider("Fire Detection Threshold", 0.0, 1.0, .5)
    option1 = st.selectbox("Phase", ["OnStation", "Option B", "Option C"])
    st.write("Following the MASC architecture the mission is divided into 5 portions.")
    option2 = st.selectbox("Swarm Baseline [Consensus]", ["Option X", "Option Y", "Option Z"])
    st.write("The algorithm which the swarm will use for consensus.")
    option3 = st.selectbox("SWARM Baseline [Motion]", ["Option Alpha", "Option Beta", "Option Kappa"])
    st.write("The algorithm which the swarm will use for motion.")
    option4 = st.selectbox("Communication Baseline [Routing Protocol]", ["Option 1", "Option 2", "Option 3"])
    st.write("The algorithm which the swarm will use for communication.")
    option5 = st.selectbox("Risk Profile", ["High Risk", "Medium Risk", "Low Risk"])
    st.write("The profile the swarm will follow.")

# Section 4: Text       (Right most column, for summary) 
with col4:
    st.header("Mission Summary")
    st.write("Mission:", option0)
    st.write("Phase:", option1)
    st.write("Swarm Baseline [Consensus]:", option2)
    st.write("Swarm Baseline [Motion]:", option3)
    st.write("Communication Baseline:", option4)
    st.write("Risk Profile:", option5)
    calculate_button = st.button("Calculate")


# Function to update the plots
# Inputs (scalable): the array of the data you want to plot, if you are adding more plots, add more inputs and figures
# By default, the x-axis is the index of the array
# This function is called after every loop, so it will update the plots in real-time (per sample calculation)
def update_plots_realtime(fireRatio, PredictionModel):
    # Generate data based on global slider values
    x1 = np.arange(fireRatio.size)
    y1 = fireRatio

    # Create the first plot
    fig1, ax1 = plt.subplots()
    ax1.plot(x1, y1)
    ax1.set_xlabel("simseconds")
    ax1.set_ylabel("% of fire detected")

    # Update the plots in the Streamlit app
    plot1_placeholder.pyplot(fig1)

    # Pause to allow time for slider updates
    plt.close(fig1)                     # Important: Close the plot to avoid memory issues

    x2 = np.arange(PredictionModel.size)
    y2 = PredictionModel

    # Create the second plot
    fig2, ax2 = plt.subplots()
    ax2.plot(x2, y2)
    ax2.set_xlabel("simseconds")
    ax2.set_ylabel("FractionCorrectDecision")

    # Update the plots in the Streamlit app
    plot2_placeholder.pyplot(fig2)

    # Pause to allow time for slider updates
    plt.close(fig2)                     # Important: Close the plot to avoid memory issues


# Check if calculate button is clicked
if calculate_button:
    # Store slider values in global variables
    startFlag = 424                                 # This is the flag to start the simulation, otherwise the simulation will start without provation and never stop
    global_slider1_value = slider1_value
    global_slider2_value = slider2_value
    global_slider3_value = slider3_value
    global_slider4_value = slider4_value
    global_slider6_value = slider6_value
    if option5 == "High Risk":
        global_dropdown1_value = 0
    if option5 == "Medium Risk":
        global_dropdown1_value = 1
    if option5 == "Low Risk":
        global_dropdown1_value = 2
    global_threshold = threshold

# Section 3: Output Plots (Bottom Row)
    with col3:  # Left most plot
        st.header("Output Plots")
        plot1_placeholder = st.empty()
    with col5:  # Middle plot
        st.header("Secondary Plots")
        plot2_placeholder = st.empty()
    with col6:  # Right most plot
        st.header("Options Summary")
        data_intial_check = np.genfromtxt('C:/Users/pando/.vscode/Repo/RobotSim/Dash/data.txt', delimiter=',')  # read from txt file to see if the data has reset 
        if data_intial_check[1].size > 10:      ## once a threshold of time (10 simseconds in this case) is reached, the simulation will provide feedback
            if data_intial_check[1][-1] < global_threshold:         # The condition for the simulation to provide feedback
                # Symbol for SensorAccuracy
                # This is where the calculation for the recommendation happens. At the moment it is a system of equations since the model is a linear model
                # This logic should be updated to match whatever model is being used (and made into a function if desired)
                SensorAccuracy = symbols('SensorAccuracy')

                # Equations for each risk level without the random noise
                eqn_high_risk = Eq(.18155 + .8941 * SensorAccuracy * 1.2, global_threshold)     # Equation for high risk (the SensorAccuracy is multiplied by 1.2 to increase the risk level)
                eqn_medium_risk = Eq(.18155 + .8941 * SensorAccuracy * 1, global_threshold)     # Equation for medium risk (the SensorAccuracy is multiplied by 1 to keep the risk level the same)
                eqn_low_risk = Eq(.18155 + .8941 * SensorAccuracy * 0.8, global_threshold)      # Equation for low risk (the SensorAccuracy is multiplied by 0.8 to decrease the risk level)

                # Solving each equation for SensorAccuracy
                threshold_high_risk = solve(eqn_high_risk, SensorAccuracy)[0]           # Solve the equation for SensorAccuracy
                threshold_medium_risk = solve(eqn_medium_risk, SensorAccuracy)[0]       # Solve the equation for SensorAccuracy
                threshold_low_risk = solve(eqn_low_risk, SensorAccuracy)[0]             # Solve the equation for SensorAccuracy

                st.write("Call the fire department")  
                # Add options of what you should change the variables to in order to get the desired output
                selected_option = st.multiselect("Change the following variables to:", ["High Risk: Sensor Accuracy = " + str(threshold_high_risk), "Medium Risk: Sensor Accuracy = " + str(threshold_medium_risk), "Low Risk: Sensor Accuracy = " + str(threshold_low_risk)])
            else: 
                st.write("Mission Status: Success")

        # Clear the file to avoid the simulation running again on boot
    with open('C:/Users/pando/.vscode/Repo/RobotSim/Dash/output.txt', 'w') as file:  
        pass


    # Create a list of strings to write to the file
    data = [startFlag, global_slider1_value, global_slider2_value, global_slider3_value, global_slider4_value, global_slider6_value, global_dropdown1_value]

    # Write the list to the file (this is where the txt file changes to have the start flag to start sims)
    np.savetxt('C:/Users/pando/.vscode/Repo/RobotSim/Dash/output.txt', data, fmt='%s')   

#####################################################################################################################################
#####################################################################################################################################
############################################### Dashboard End #######################################################################

## main loop. Treat this is a while(1==1) loop

loadedData = np.loadtxt('C:/Users/pando/.vscode/Repo/RobotSim/Dash/output.txt', usecols=0)  ## Configuration file
flag = loadedData[0]            ## start flag is the first value (if 424, start the simulation)
data_intial = np.genfromtxt('C:/Users/pando/.vscode/Repo/RobotSim/Dash/data.txt', delimiter=',')    ## Data file to plot
fireRatio = data_intial[0]          ## fireRatio is the first row
PredictionModel = data_intial[1]       ## PredictionModel is the second row

if flag == 424:

    with open('C:/Users/pando/.vscode/Repo/RobotSim/Dash/output.txt', 'w') as file:  
        pass

    startFlag = 000     # set the start flag to 000 to avoid the simulation running again on boot

    # Data from global and configuration file
    data = [startFlag, global_slider1_value, global_slider2_value, global_slider3_value, global_slider4_value, global_slider6_value, global_dropdown1_value]
    CommunicationRange = global_slider4_value
    SensorAccuracy = global_slider3_value
    NumBots = global_slider1_value
    time = global_slider6_value
    Risk = global_dropdown1_value

    # This is the output model which is the ML model that will be used to predict the consensus
    # This also incorporates Risk as a option
    # At the moment we are adding random noise to the output to compensate for uncertainty in our model (this should be removed in the final version)
    def output_model(Risk, NumBots, SensorAccuracy, CommunicationRange):        # EQN AND COEFFICIENTS COME FROM THE ML MODEL
        if Risk == 0:     #High Risk
            coeffBots = .7
            coeffSens = 1.2
            eqn = .18155 + 0 * NumBots * coeffBots + .8941 * SensorAccuracy * coeffSens + 0 * CommunicationRange + float(np.random.normal(0, .005, 1))
            if eqn > 1:
                eqn = 1
        if Risk == 1:     #Medium Risk
            coeffBots = .9
            coeffSens = 1
            eqn = .18155 + 0 * NumBots * coeffBots + .8941 * SensorAccuracy * coeffSens + 0 * CommunicationRange + float(np.random.normal(0, .005, 1))
            if eqn > 1:
                eqn = 1
        if Risk == 2:     #Low Risk
            coeffBots = 1
            coeffSens = .8
            eqn = .18155 + 0 * NumBots * coeffBots + .8941 * SensorAccuracy * coeffSens + 0 * CommunicationRange + float(np.random.normal(0, .005, 1))
            if eqn > 1:
                eqn = 1
        return eqn



    # Write the list to the file
    np.savetxt('C:/Users/pando/.vscode/Repo/RobotSim/Dash/output.txt', data, fmt='%s')   ## Write the data to the file, more importantly the start flag to avoid the simulation running again on boot
    while (fireRatio.size < time):      # Time is the alotted time for the simulation
        # Read data from the txt file
        fireRatio = np.append(fireRatio, round((random.random() * 10), 2))
        if PredictionModel.size < int(time/2):      ## currently we are investigating what would happend if at 50% of the mission time we change the model (different research questions can be posed with this setup)
            PredictionModel = np.append(PredictionModel, output_model(Risk, NumBots, SensorAccuracy, CommunicationRange))
        else:
            PredictionModel = np.append(PredictionModel, output_model(0, NumBots, SensorAccuracy, CommunicationRange))
        
        # Open a file in write mode this entire process is very picky about datatypes (avoid changing this unless you need to)
        with open('C:/Users/pando/.vscode/Repo/RobotSim/Dash/data.txt', 'w') as file:
            # Iterate through the array
            file.write(','.join(map(str, fireRatio)) + '\n')
            file.write(','.join(map(str, PredictionModel)))
        data = np.genfromtxt('C:/Users/pando/.vscode/Repo/RobotSim/Dash/data.txt', delimiter=',')
        update_plots_realtime(np.array(data[0]), np.array(data[1]))    ##send to update realtime plots on runtime
    # This will clear the file after the while is done, which means the simulation ended (notice this is outside the while loop)
    with open('C:/Users/pando/.vscode/Repo/RobotSim/Dash/data.txt', 'w') as file:
        # Initialize the file with zeros to avoid errors reading null txt file
        file.write('0' + '\n')
        file.write('0')

## The dashboard cannot be run locally, meaning from vscode or any code editor you need to run this from the command line
## The command to run this is depends on how you have configured your python environment
## These are the two scenarios that I have ran into (1st is using anaconda and 2nd is using the python environment) {try both and see which one works}:
## format: streamlit {function/library} run {command} file location {file location} 

## PC: streamlit run c:/Users/pando/.vscode/Repo/RobotSim/Dash/DashOnlyModern.py
## Laptop: python -m streamlit run c:/Users/pando/.vscode/Repo/RobotSim/Dash/DashOnlyModern.py
          