import csv
import numpy as np
import matplotlib.pyplot as plt

# Create a dictionary to hold the data
#data_dict = {(x, y, 5): [] for x in range(5, 10) for y in range(10, 20)}
filename = 'testPP.csv'

##note be careful with the datatypes: they will always assume they are strings
def csv2D(filename):
    with open(filename, mode = 'r') as f:         ##keeping this up here to be able to read each cell of a csv to my liking 
        csv2d = csv.reader(f)                       ##remember to change the name of the file to match 
        csv2d  = list(csv2d)
    return csv2d

def max_finder(filename, column_index):             ##use this to get the index which the data dict will range from 
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        max_value = max(int(row[column_index]) for row in reader)
    return max_value

def min_finder(filename, column_index):             ##use this to get the index which the data dict will range from 
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        max_value = min(int(row[column_index]) for row in reader)
    return max_value

thisIsFun = csv2D(filename)
#print(thisIsFun)
#print(thisIsFun[0])
#print(thisIsFun[0][0] == 1)


minBots = min_finder(filename, 0)
maxBots = max_finder(filename, 0)

minSize = min_finder(filename, 1)
maxSize = max_finder(filename, 1)

data_dict = {(x, y, 5): [] for x in range(minBots, maxBots) for y in range(minSize, maxSize)}

def fill_table(csv):                         ##takes the empty directory and fills it
    for row in csv:
        key = (int(row[0]), int(row[1]), 5)
        if key in data_dict:
            data_dict[key].append(int(row[3]))
        else:
            data_dict[key] = [int(row[3])]
    return data_dict


def filter_data(direc):
    Output = []
    combinations = [(x, y,5) for x in range(minBots, maxBots) for y in range(minSize, maxSize)]
    for combo in combinations:
        #print("this is combo output RAW:", data_dict[combo])
        direc[combo] = [value for value in direc[combo] if value != 1001]       ##removing the 1001 
        #print("this is combo output without 1001's:", data_dict[combo])
        direc[combo] = np.median(direc[combo]) + combo[0]*3.5 + combo[1]*1.5  ##cost analysis
        ##direc[combo] = np.median(direc[combo])   ##raw
        print("this is combo output medianed:",direc[combo])    ##filtered Data
        Output.append(direc[combo])
    formatted_data = np.array(Output).reshape((maxBots-minBots), (maxSize-minSize))
    return data_dict, formatted_data

new_dict = fill_table(thisIsFun)
print(new_dict)
filtered_data, fomratted_data = filter_data(new_dict)

# Create the imshow plot
plt.imshow(fomratted_data, extent=[minSize, maxSize, minBots, maxBots],
           origin='lower', aspect='auto', cmap='viridis', vmin= 50, vmax= 150)

# Add colorbar for better visualization
plt.colorbar()

# Add labels and title
plt.xlabel('SensingArea')
plt.ylabel('NumBots')
plt.title('Median Amount of Time (ticks) to Detect 95% of the Fire')

plt.show()