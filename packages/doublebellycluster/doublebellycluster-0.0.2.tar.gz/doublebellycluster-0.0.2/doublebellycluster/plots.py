

import matplotlib.pyplot as plt
import numpy as np


def plot_color_map( df, name, show_save = True):
    fig, ax = plt.subplots()
    scatter_x = np.array(df.iloc[:,0])
    scatter_y = np.array(df.iloc[:,1])
    group = np.array(df.iloc[:,2])

    for g in np.unique(group):
        i = np.where(group == g)
        ax.scatter(scatter_x[i], scatter_y[i], label=g)
    ax.legend()
    
    if show_save:
        plt.show()
    else:
        fig.savefig(f'C:/Users/User/Desktop/{name}.png')

