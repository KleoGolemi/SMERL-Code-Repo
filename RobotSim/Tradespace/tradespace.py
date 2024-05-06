import tkinter as tk        
from tkinter import ttk    ## This is needed to create the dropdown menu (Simplistic GUI)
import os     ## This is needed to check if the file path exists
import RiskPlotTradespace as rpt        ## This is the file which will plot the data

# Function to get the current selections (dropdown menu and checkboxes)
def get_selections():
    selected_risk_profile = risk_profile_var.get()
    selected_output = output_var.get()
    selected_options = {option_labels[i]: var.get() for i, var in enumerate(checkbox_vars)} # Robots, Sensor Accuracy, Communication Range, Disabled Robots

    print("Selected Risk Profile:", selected_risk_profile)
    print("Selected Output:", selected_output)
    print("Selected Options:", selected_options)
    selected_options = list(selected_options.values())
    ## see which indes is set to 1
    selected_options = [i for i, x in enumerate(selected_options) if x == 1]
    print("Selected Options:", selected_options)
    print(len(selected_options))
    
    # Determine the file path based on selections
    file_path = "path/to/default.csv"  # Default file path
    
    # Given inputs navigate to the correct file path to read from, these paths need to be standardized and filled with proper data
    if selected_risk_profile == "Low":
        file_path = "RobotSim\Tradespace\Data\Low Risk\dataTest1000_10Bins.csv"      
    elif selected_risk_profile == "Medium":
        file_path = "RobotSim\Tradespace\Data\Medium Risk\MediumRisk_10Bins.csv"
    elif selected_risk_profile == "High":
        file_path = "RobotSim\Tradespace\Data\High Risk\highrisk2-20bins-675fire.csv"
    
    # Read data from the CSV file and display in a plot
    if os.path.exists(file_path):
        print("Reading data from:", file_path)
        rpt.plot_tradespace(file_path, selected_options)            
    else:       
        print("File not found:", file_path)

    

# Create the main window
root = tk.Tk()
root.title("Risk Profile, Options, and Output")

# Dropdown for risk profile selection
risk_profile_var = tk.StringVar()
risk_profile_label = tk.Label(root, text="Select Risk Profile:")
risk_profile_label.pack()
risk_profiles = ["Low", "Medium", "High"]
risk_profile_dropdown = ttk.Combobox(root, textvariable=risk_profile_var, values=risk_profiles)
risk_profile_dropdown.pack()

# Checkboxes for specific options
checkbox_vars = [tk.IntVar() for _ in range(4)]
option_labels = ["Robots", "Sensor Accuracy", "Communication Range",  "Disabled Robots"]
options_frame = tk.Frame(root)
options_frame.pack()
for i, label in enumerate(option_labels):
    tk.Checkbutton(options_frame, text=label, variable=checkbox_vars[i]).pack(anchor=tk.W)

# Dropdown for output selection
output_var = tk.StringVar()
output_label = tk.Label(root, text="Select Output:")
output_label.pack()
output_options = ["FractionCorrectDecision"]  # Customize these options as needed
output_dropdown = ttk.Combobox(root, textvariable=output_var, values=output_options)
output_dropdown.pack()

# Button to get selections
selection_button = tk.Button(root, text="Get Selections", command=get_selections)
selection_button.pack()

root.mainloop()

"""
For this interface there are three options: High, Medium, and Low Risk.
Within the options, there are four checkboxes: Robots, Sensor Accuracy, Communication Range, and Disabled Robots.
The output options are FractionCorrectDecision, which will generate a plot given the information which you provide.
Once the selections are made, the Get Selections button will go through the neccessary file path to get to the needed file.
Once at the file it will read through the csv only the data which the user selected and display it in a plot.
NOTE: Since they are not standardized at the moment the code will read the number of columns, if its 4, then you cant show robot disabled, if its 5 then you can show robot disabled.
NOTE: Ideally each option takes you through a folder path to get to a singular csv file, which will be read and displayed in a plot.
"""