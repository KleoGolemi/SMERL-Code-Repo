import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D # Used for 3D plots
import mplcursors           # Used for hover-over annotations

def load_data(file_path, num_columns):
    if num_columns == 5:
        column_names = ['NumBots', 'Sensor Accuracy', 'Comm. Range', 'Bots Disabled', 'FracCorrectDecisions']
    elif num_columns == 4:
        column_names = ['NumBots', 'Sensor Accuracy', 'Comm. Range', 'FracCorrectDecisions']
    else:
        raise ValueError("Invalid number of columns in the CSV file")
    
    return pd.read_csv(file_path, header=None, names=column_names)


##this is the 2d plot, you plot the mean output vs the input variable selected (DOE methodology)
def plot_2d(data, x_col, y_col, std_col, title):         
    scatter = plt.scatter(data[x_col], data[y_col], c=data['mean'], cmap='viridis', zorder=2)
    cbar = plt.colorbar(scatter, shrink=0.5, aspect=5)
    cbar.set_label('Mean Output')
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(title)

    # Add hover-over annotations
    def on_plot_hover(sel):
            sel.annotation.set_text(f'Mean: {data["mean"][sel.target.index]:.2f}, Std: {data["std"][sel.target.index]:.2f}')
    mplcursors.cursor(scatter).connect("add", on_plot_hover)

    plt.show()

##this is the 3d plot, you plot the mean output vs the input variables selected (DOE methodology)
## Note you cannot express variance in a 3d plot so you can only plot the mean output (if you do that will be the size which is bad cuz if variance is low the datapoint will dissapear)
def plot_3d(data, x_col, y_col, z_col, title):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(data[x_col], data[y_col], data[z_col], c=data['mean'], cmap='viridis')
    cbar = plt.colorbar(scatter, shrink=0.5, aspect=5)
    cbar.set_label('Mean Output')
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_zlabel(z_col)
    plt.title(title)

    # Add hover-over annotations
    def on_plot_hover(sel):     
            sel.annotation.set_text(f'Mean: {data["mean"][sel.target.index]:.2f}, Std: {data["std"][sel.target.index]:.2f}')    # Variance is displayed in the hover-over annotation
    mplcursors.cursor(scatter).connect("add", on_plot_hover)

    plt.show()


"""
This function reads a CSV file and plots the trade space based on the input index to plot
The index to plot is a list of the column indices to plot
For example, if you want to plot the trade space for the first column, you would pass [0] as the index_to_plot
"""
def plot_tradespace(file_path, index_to_plot):
    df = pd.read_csv(file_path, header=None)
    num_columns = df.shape[1]
    data = load_data(file_path, num_columns)

    grouped = data.groupby(data.columns[:len(data.columns)-1].tolist())['FracCorrectDecisions'].agg(['mean', 'std']).reset_index()
    
    input_cols = grouped.columns[index_to_plot]
    print(input_cols)

    max_mean = grouped['mean'].max()
    max_mean_index = grouped['mean'].idxmax()
    print('Max Mean:', max_mean)
    print('Max Mean Index:', max_mean_index)

    if len(index_to_plot) == 3:
        plot_3d(grouped, *input_cols, '3D Plot of DOE with Mean Output and Std Deviation')
        
    elif len(index_to_plot) == 2:
        plot_2d(grouped, *input_cols, 'std', '2D Plot of DOE with Mean Output and Std Deviation')

    elif len(index_to_plot) == 1:
        x_col = input_cols[0]
        y_col = 'mean'
        std_dev = 'std'

        x = grouped[x_col].values.astype(float)
        y = grouped[y_col].values.astype(float)
        std_dev = grouped[std_dev].values.astype(float)

        plt.errorbar(x, y, yerr=std_dev, fmt='o', color='black', ecolor='lightgray', elinewidth=3, capsize=0)
        plt.xlabel(x_col)
        plt.ylabel('Mean Output')
        plt.title('Mean Output vs. ' + x_col)
        plt.show()

if __name__ == "__main__":      ## This is just for debugging. This file is called to tradespace so this line will never execute unless you run this file
    plot_tradespace('RobotSim\Tradespace\Data\Low Risk\dataTest1000_10Bins.csv', [0])
