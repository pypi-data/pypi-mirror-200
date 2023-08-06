
import math
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.metrics.pairwise import pairwise_distances

import matplotlib.pyplot as plt
import random

warnings.filterwarnings("ignore")



xy = pd.read_csv('C:/Users/User/Desktop/dus.csv', index_col=0)
xy.columns = [0,1, 'y']


check_array = np.array([0.1, 0.8, 0.1])


def do_nearby_cluster(check_array, xy, ):

    sub_deveied_data = xy.groupby('y')[[0,1]].mean().reset_index()
    xy = pd.concat([xy,sub_deveied_data],axis = 0)

    print(xy)

    nun = xy['y'].nunique()
    d_matrix = pd.DataFrame(pairwise_distances(xy[[0,1]].iloc[-nun:,:],xy[[0,1]].iloc[:-nun,:]) )
    print(d_matrix)


    d = [[] for i in range(nun)]
    count =0 
    while count < xy.shape[0] - sub_deveied_data.shape[0]:
        
        if count%100 == 0:
            num_array =[]
            for i in range(nun):
                num_array += [len(d[i])]
            num_array = np.array(num_array)
            num_array = num_array / num_array.sum()
            print(num_array)

            n_where_num = num_array - check_array <= -0.01
            

            if sum(n_where_num) == 0:
                n_where_num[random.randrange(nun)] = True
            print(count)
            

        for i in range(nun):
            if n_where_num[i]:
                ind = d_matrix.iloc[i,:].idxmin()
                if math.isnan(ind) == False:
                    d[i] += [ind]
                    d_matrix.iloc[:,ind]= np.nan

                    count +=1
        
    num_array =[]
    for i in range(nun):
        num_array += [len(d[i])]
    num_array = np.array(num_array)
    num_array = num_array / num_array.sum()
    print(num_array)

    col = [[check_array[k] for k, j in enumerate(d) if i in j][0] for i in range(xy.shape[0]-3)]
    
    return col


xy['col'] = do_nearby_cluster(check_array, xy)

def plot_color_map(df):
    global file_name
    fig, ax = plt.subplots()
    scatter_x = np.array(df.iloc[:,0])
    scatter_y = np.array(df.iloc[:,1])
    group = np.array(df.iloc[:,2])

    for g in np.unique(group):
        i = np.where(group == g)
        ax.scatter(scatter_x[i], scatter_y[i], label=g)
    ax.legend()
    fig.savefig(f'C:/Users/User/Desktop/data_.png')

plot_color_map(xy[[0,1,'col']])

