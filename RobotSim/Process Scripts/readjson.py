import numpy as np
import matplotlib.pyplot as plt
import os
"""
This is for Crosscombe
"""
def find_all(string, file_contents):
    indexOfInterest = []
    for i, content in enumerate(file_contents):
        if string == content:
            indexOfInterest.append(i)
    return indexOfInterest
"""
This function takes the json belief value and returns the fraction of correct decisions.
Right now this function works for 10 bins, so +/- 5% of the value
To be tested with other numbers of bins
"""
def BelieftoFCD(value, frr):
    frr = .1
    if value == 2:
        return 1
    if '2' not in str(value):
        return -1
    else:
        newvalue = np.log10(int(value/20))
        output = 1 - (frr*newvalue + .1)
        return output ##returns the upper limit value fraction of correct decisions so if output is .7 thats (.6-.7)
    
"""
This function is takes the fractioncorrectdecisions value and returns the json value to match.
Right now this function works for 10 bins, so +/- 5% of the value.
To be tested with other numbers of bins.
"""    
def FCDtoBelief(output, frr):
    frr = 0.1
    if output == 1:
        return 2
    elif output == -1:
        return None  # No valid input for output -1
    else:
        newvalue = np.ceil((1 - output - 0.1) / frr)
        value = 20 * 10**newvalue
        return int(value)

    

"""
This functions takes the value of all robots at all timestamps and returns the fraction of correct decisions at each timestamp
"""
def fractioncorrectdecisions(arrayofdata, tfr, ffr):
    # print("This is: ", np.ceil(tfr *10)/10)
    # print("Belief: ", FCDtoBelief(np.ceil(tfr * 10) / 10, ffr))
    arrayofFracCorrectDecisions = np.array(np.zeros(len(arrayofdata[0])))
    for timestamp in range(len(arrayofdata[0])):
        for robot in arrayofdata:
            if robot[timestamp] == FCDtoBelief(np.ceil(tfr * 10) / 10, ffr):
                arrayofFracCorrectDecisions[timestamp] += 1
            else:
                pass
    arrayofFracCorrectDecisions = [x/len(arrayofdata) for x in arrayofFracCorrectDecisions]
    return arrayofFracCorrectDecisions

def fractioncorrectdecisions_ebert(arrayofdata):
    arrayofFracCorrectDecisions = np.array(np.zeros(len(arrayofdata[0])))
    for timestamp in range(len(arrayofdata[0])):
        for robot in arrayofdata:
            if robot[timestamp] == 1:
                arrayofFracCorrectDecisions[timestamp] += 1
            else:
                pass
    arrayofFracCorrectDecisions = [x/len(arrayofdata) for x in arrayofFracCorrectDecisions]
    return arrayofFracCorrectDecisions

def process_ebert(file):
    json_lines = []
    with open(file, 'r') as file:      ##treat json as text
        for line in file:
            json_lines.append(line.strip())
    
    # print(json_lines[0:10])
    
    indexOfInterest_start = find_all('[', json_lines)
    indexOfInterest_end = find_all('],', json_lines)
    indexOfInterest_start = indexOfInterest_start
    indexOfInterest_end = indexOfInterest_end
    indexOfInterest_end.append(len(json_lines)-3)
    
    # print(len(indexOfInterest_start))
    # print(len(indexOfInterest_end))
    # print(indexOfInterest_start)
    # print(indexOfInterest_end)
    
    ##index of interest start has data 1 index after the value
    ##index of interest end has data -1 indexes before the value
    """
    The data is partitioned into an array of arrays which would represent the different robots and their data per timestep
    """
    partitioned_data = []
    for i in range(len(indexOfInterest_end)):
        partitioned_data.append(json_lines[indexOfInterest_start[i]+1:indexOfInterest_end[i]-1])          ##start 1 after the flag until the end
        ##at this point partitioned_data[i] is an entire bots beleif over time
        ##next we will filter through to extract just the output
        partitioned_data[i] = [item for item in partitioned_data[i] if item != '']  ##remove empty strings
        partitioned_data[i] = [item[-4:-2] for item in partitioned_data[i]]
        ##remove ',' in string then make int
        partitioned_data[i] = [int(s.replace(',', '')) for s in partitioned_data[i]]  ##make them ints
        partitioned_data[i] = [int(item) for item in partitioned_data[i]]  
        
    output = fractioncorrectdecisions_ebert(partitioned_data)   ##given the an array of robot beliefs over time, return the fraction of correct decisions per time step
    return output

def process_crosscombe(file):
    json_lines = []
    with open(file, 'r') as file:      ##treat json as text
        for line in file:
            json_lines.append(line.strip())
            
    # print(json_lines[0:10])
    ##extraxt only the numbers 
    tfr = float(json_lines[8].split(' ')[-1].replace(',', ''))  ##extract the tfr value
    ffr = float(json_lines[9].split(' ')[-1].replace(',', ''))  ##extract the ffr value

    """
    This is where you find the index of the start and end of the data you want to parse
    """
    indexOfInterest_start = find_all('[', json_lines)
    indexOfInterest_end = find_all('],', json_lines)
    indexOfInterest_start = indexOfInterest_start
    indexOfInterest_end = indexOfInterest_end
    indexOfInterest_end.pop(0)
    indexOfInterest_end.append(len(json_lines)-3)

    ##index of interest start has data 1 index after the value
    ##index of interest end has data -1 indexes before the value

    """
    The data is partitioned into an array of arrays which would represent the different robots and their data per timestep
    """
    partitioned_data = []
    for i in range(len(indexOfInterest_end)):
        partitioned_data.append(json_lines[indexOfInterest_start[i]+1:indexOfInterest_end[i]-1])          ##start 1 after the flag until the end
        ##at this point partitioned_data[i] is an entire bots beleif over time
        ##next we will filter through to extract just the output
        partitioned_data[i] = [item for item in partitioned_data[i] if item != '']  ##remove empty strings
        partitioned_data[i] = [int(''.join(char for char in s.rstrip() if char.isdigit())) for s in partitioned_data[i]]  ##make them ints

    
    # print(partitioned_data[0])
    output = fractioncorrectdecisions(partitioned_data, tfr, ffr)  ##given the an array of robot beliefs over time, return the fraction of correct decisions per time step
    return output
        

# Read the JSON file as text
# Read the JSON file and print each line
if __name__ == "__main__":
    ##################################################################### CROSSCOMBE #####################################################################

    ##Proccess the entire folder
    folder = 'c:/Users/pando/Downloads/021324_002744_t100_s5000_tfr650-0-650_frr100-400-500_opt10'  # Replace with the actual folder path
    output_crosscombe = []
    for file in os.listdir(folder):
        if file.endswith('.json'):
            file_path = os.path.join(folder, file)
            output_crosscombe.append(process_crosscombe(file_path))
    print(len(output_crosscombe))
    output_crosscombe = np.mean(output_crosscombe, axis = 0)
    print(len(output_crosscombe))
    
    ##################################################################### EBERT #####################################################################
    output_ebert = []
    folder = 'C:/Users/pando/Downloads/021424_161450_t100_s5000_tfr650-0-650_sp675-0-675_prior10_thrsh990_posfb0'
    for file in os.listdir(folder):
        if file.endswith('.json'):
            file_path = os.path.join(folder, file)
            output_ebert.append(process_ebert(file_path))
    print(len(output_ebert))
    output_ebert = np.mean(output_ebert, axis = 0)
    print(len(output_ebert))
    
    plt.scatter(range(len(output_crosscombe)), output_crosscombe, label = 'Crosscombe')
    plt.scatter(range(len(output_ebert)), output_ebert, label = 'Ebert')
    plt.legend()
    plt.grid()
    plt.title('Fraction of Correct Decisions')
    plt.xlabel('Time')
    plt.ylabel('Fraction of Correct Decisions')
    plt.show()
    


        