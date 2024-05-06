import os
import csv

####Parameters to Extract
##this file will read a folder filled with argos csv data outputs and extract the last reading of 'fractioncorrectdecision' into a csv dataTest

def readCSV(filename, *args):
    saveData = {}
    with open(filename, mode='r') as f:
        mycsv = csv.reader(f)
        mycsv = list(mycsv)
        for arg in args:
            saveRow = []
            saveCol = []
            for counter_row, row in enumerate(mycsv):  # Use enumerate to get both row index and row data
                for counter_column, row_item in enumerate(row):  # Use enumerate to get both column index and column data
                    if row_item.strip() == arg:
                        saveRow.append(counter_row)
                        saveCol.append(counter_column)

            saveData[arg] = [mycsv[x] for x in saveRow if x < len(mycsv)]  # Check if index is within valid range

    return saveData

def writeData(saveData, search_terms, time_flag):
    for search_term in search_terms:
        if search_term == 'fractioncorrectdecisions':       ## The output
            
            if time_flag == 1:
            
                data = []
                last10points = saveData[search_term][-10:]  # Take the last 10 points (change per application)
                print("This is frac: ", last10points)
                print("This is frac: ", last10points[0][2])  # [0][2]
                # for entry in last10points pull out the value which is the last element in the list
                for entry in last10points:
                    data.append(float(entry[2]))  # Convert the string to float
                    print("This is data: ", data)

            if time_flag == 0:                  ## depending on what the format of the argos csv is you may need to change this
                last10points = saveData[search_term][-1:]
                last10points = saveData[search_term][-1:]           ##[-1:]
                print("This is frac: ", last10points)
                print("This is frac: ", last10points[0][2])         ##[0][2]
                data = str(last10points[0][2])              ##[0][2]
        if search_term == 'robots':         ## lazy naming convention but for the parameters there is only 1 value so looking at the last index is just as valid
            last10points = saveData[search_term][-1:]
            print(last10points[0][2])
            NumBots = str(last10points[0][2])
        if search_term == 'range':
            last10points = saveData[search_term][-1:]
            print(last10points[0][2])
            CommRange = str(last10points[0][2])
        if search_term == 'sensorprob':
            last10points = saveData[search_term][-1:]
            print(last10points[0][2])
            sensorprob = str(last10points[0][2])
        if search_term == 'motion_disabled':
            last10points = saveData[search_term][-1:]
            print(last10points[0][2])
            disable = str(last10points[0][2])
        if search_term == 'simseconds':
            last10points = saveData[search_term][-1:]
            print(last10points[0][2])
            simseconds = str(last10points[0][2])

    if time_flag == 1:
        DATA = [NumBots, sensorprob, CommRange, disable, simseconds, data]          ## format writing to output csv file from processing folder if you want time marks
    if time_flag == 0:
        DATA = [NumBots, sensorprob, CommRange, disable, data]      ## format writing to output csv file from processing folder if you dont want time marks
    # File path to save the CSV file
    file_path = 'highrisk2-20bins-675fire.csv'           ##Change this per run (LOCATION TO WRITE TO)

    # Write the data to the CSV file
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(DATA)                          ##make this write rows for when you have to write more than 1 row
    print(DATA)
    
if __name__ == "__main__":
    folder_path = 'c:/Users/pando/Downloads/experiment_output'  # Replace this with the path to the folder you want to list (LOCATION OF THE FOLDER TO READ FROM -- FOLDER NOT ZIP FILE)

    # List all files in the folder
    file_list = os.listdir(folder_path)
    for file in file_list:
        saveRow = []
        saveCol = []
        saveData = readCSV(folder_path +'/' + file, 'range', 'speed', 'robots', 'fillratio', 'sensorprob', 'motion_disabled', 'simseconds', 'fractioncorrectdecisions')
        search_terms = list(saveData.keys())  # Convert dictionary keys to a list
        writeData(saveData, search_terms, time_flag=0)      ## NOTE: Remember flag and if time_flag = 1 then go to compress.py continue to tradespace.py

    print("DONE")

## Plotting the data can be done independently in a different script or under the tradespace folder