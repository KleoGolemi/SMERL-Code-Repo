"""
Given a csv with time logs, it will show you the FCD (FractionCorrectDecision) as a function of time from the available options
In this file you take a CSV file and convert the FCD column to a list of lists.
Then you group the data by the input parameters and calculate the mean of the FCD column for each group.
Finally, you save the result to a new CSV file and graph as needed.
This gets funky with the variables from the csv being read a str not arrays or floats so you have to convert them to the right type with 'ast'
"""

import pandas as pd
import ast
import numpy as np

# Load the data
data = pd.read_csv('RobotSim/Tradespace/Data/High Risk/highrisk2-20bins-675fire_wTimesteps.csv', header=None)       #NOTE: Change this to the path of the file you want to read
data.columns = ['Bots', 'Sensor', 'CommRange', 'Disable', 'TotalTime', 'FCD']

# Convert the 'FCD' column values from string representation of lists to actual lists
data['FCD'] = data['FCD'].apply(ast.literal_eval)

# Split the CSV into groups of the same input parameters
data_grouped = data.groupby(['Bots', 'Sensor', 'CommRange', 'Disable'])

# Compute the mean of the 'FCD' column for each group preserving multiple values
mean_values = data_grouped['FCD'].apply(lambda x: np.mean(x.tolist(), axis=0))

# Reset the index to have a DataFrame with columns for group identifiers and mean values
mean_values = mean_values.reset_index()

# Calculate std deviation
std_values = data_grouped['FCD'].apply(lambda x: np.std(x.tolist(), axis=0))
std_values = std_values.reset_index()


# Save the result to new CSV file
mean_values.to_csv('RobotSim/Tradespace/Data/High Risk/highrisk2-20bins-675fire_wTimesteps_mean.csv', index=False)  #NOTE: Change this to the path of the file you want to save
std_values.to_csv('RobotSim/Tradespace/Data/High Risk/highrisk2-20bins-675fire_wTimesteps_std.csv', index=False)    #NOTE: Change this to the path of the file you want to save

# Show a list of options for the user to select
import tkinter as tk
from tkinter import ttk
import os
import csv
import matplotlib.pyplot as plt

"""
This function goes through the compressed csv file and finds the rows that match the user inputs (it should only find 1)
"""
def search_csv(file_path, value1, value2, value3, value4):
    found_rows = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if value1 in row and value2 in row and value3 in row and value4 in row:
                found_rows.append(row)
    return found_rows

# Show all the unique values for each variable
bots_values = mean_values['Bots'].unique()
sensor_values = mean_values['Sensor'].unique()
comm_range_values = mean_values['CommRange'].unique()
disable_values = mean_values['Disable'].unique()

print("Bots values:", bots_values)
print("Sensor values:", sensor_values)
print("CommRange values:", comm_range_values)
print("Disable values:", disable_values)

# Function to create dropdown menu for a given variable
def create_dropdown(master, label_text, values):
    label = tk.Label(master, text=label_text)
    label.pack()
    
    dropdown_var = tk.StringVar(master)
    dropdown_var.set(values[0])  # Set default value
    
    dropdown = tk.OptionMenu(master, dropdown_var, *values)
    dropdown.pack()
    
    return dropdown_var

# Create the main window
root = tk.Tk()
root.title("Dropdown Menu Example")

# Create dropdown menus for each variable
bots_dropdown_var = create_dropdown(root, "Bots:", bots_values)
sensor_dropdown_var = create_dropdown(root, "Sensor:", sensor_values)
comm_range_dropdown_var = create_dropdown(root, "CommRange:", comm_range_values)
disable_dropdown_var = create_dropdown(root, "Disable:", disable_values)

# Function to get selected values
def get_selected_values():
    bots_selected = bots_dropdown_var.get()
    sensor_selected = sensor_dropdown_var.get()
    comm_range_selected = comm_range_dropdown_var.get()
    disable_selected = disable_dropdown_var.get()
    
    print("Bots selected:", bots_selected)
    print("Sensor selected:", sensor_selected)
    print("CommRange selected:", comm_range_selected)
    print("Disable selected:", disable_selected)

    # Given these input varibles read the csv and plot the data the matches the inputs
    # Read data from the CSV file and display in a plot
    # Read the CSV file
    df = pd.read_csv('RobotSim\Tradespace\Data\High Risk\highrisk2-20bins-675fire_wTimesteps_mean.csv')  # Replace 'your_file.csv' with the path to your CSV file

    # User inputs
    user_inputs = [bots_selected, sensor_selected, comm_range_selected, disable_selected]

    # Find the row that matches the user inputs
    found_rows = search_csv('RobotSim\Tradespace\Data\High Risk\highrisk2-20bins-675fire_wTimesteps_mean.csv', *user_inputs)    
    # The output is the last input of this row, which is saved as a string
    output = found_rows[0][-1]    
    print("Output:", output)
    # the string does not have commas so when you call ast.literal_eval it will not work
    output = output.replace(" 0", ",0")     ## for values that start with 0.xxxx it will not have a comma so we need to add it
    output = output.replace(" 1", ",1")     ## for values that start with 1.000 it will not have a comma so we need to add it
    output = ast.literal_eval(output)    ## convert the string to a list
    # Plot the output (potentially make a new figure for each plot)
    plt.plot(output)
    plt.grid()
    plt.xlabel('Time')
    plt.ylabel('FCD')
    plt.show()
    

# Button to get selected values
get_values_button = tk.Button(root, text="Get Selected Values", command=get_selected_values)
get_values_button.pack()

root.mainloop()