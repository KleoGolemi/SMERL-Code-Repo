import csv 
import numpy as np
import matplotlib.pyplot as plt

def readCSV(filename):                          ##this is how you read a csv as a 2d array
    with open(filename, mode = 'r') as f:
        index = []
        data_median = []
        counter_x = 0
        counter_y = 0
        mycsv = csv.reader(f)
        mycsv = list(mycsv)
        #print(mycsv)
        #print(len(mycsv))                         ##number of rows
        #print(len(mycsv[0]))                      ##number of units of the xth row
        """
        for row in mycsv:                         ##forloop that reads the array
            for row_item in row:
                print(str(counter_y) + ', ' + str(counter_x) + ': ' + row_item)   ##to stay consistent with the thing above
                counter_x += 1
            counter_y += 1
            counter_x = 0
        """
        for row in mycsv:
            row = [int(x) for x in row]
            index.append(row[1])
            data_median.append(np.median(row[2:len(row)-1]))
            #plt.hist(row, bins= 20)
            #plt.show()
        return index, data_median

index, data_median = readCSV('RobotSim\data.csv')

print(index)
print(data_median)

plt.figure(1)
plt.grid()
plt.title("Median ticks vs Num robots [100 per point]")
plt.xlabel("Num. Bots")
plt.ylabel("Ticks")
plt.scatter(index, data_median)
plt.show()