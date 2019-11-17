# Generate a sine vs cosine curve.

import numpy as np
import matplotlib.pyplot as plt


def __main__():
    # Prepare the data
    x = np.linspace(-5, 5, 100)

    # Plot the data
    plt.plot(x, np.sin(x), color='blue', label='sine')
    plt.plot(x, np.cos(x), color='red', label='cosine')
    plt.plot(x, x - x, color='black', label='X-Axe')
    plt.plot(x - x, x, color='black', label='Y-Axe')

    # Add a legend
    plt.legend()

    # Show the plot
    plt.show()


__main__()
