import numpy as np
import matplotlib.pyplot as plt

# Create 1D data
x = np.linspace(0, 1, 10)
values = np.random.rand(10)  # Values representing color

# Create a colormap
cmap = plt.cm.viridis

# Create the plot using imshow
fig, ax = plt.subplots()
ax.imshow([values], cmap=cmap, aspect='auto')

# Set the y-axis limits
ax.set_ylim(0, .5)
ax.set_yticks([])

# Set axis labels
ax.set_xlabel('X-axis')

# Add a colorbar legend
cbar = plt.colorbar(ax.imshow([values], cmap=cmap, aspect='auto'), ax=ax)
cbar.set_label('Color Value')

# Show the plot
plt.show()
