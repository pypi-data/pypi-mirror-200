
import copy
from functools import reduce

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyproj
import scipy.stats as st
from sklearn.cluster import DBSCAN
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics.pairwise import pairwise_distances

import itertools

proj_wgs84 = pyproj.Proj(init="epsg:4326")
proj_gk4 = pyproj.Proj(init="epsg:20015")


from inter_dist import get_inter_dist
from plots import plot_color_map




class Doubleclustering:

    def __init__(self):
        self.working = True


    def d3plot(self, xy, n, show_save = True):


        xy['x'] = xy['xx'].to_list()
        xy['y'] = xy['yy'].to_list()

        xy[['x','y']] -= xy[['x','y']].min()
        xy[['x','y']] /= xy[['x','y']].max()

        # getting xy
        self.xy = xy

        xx, yy = np.mgrid[0:1:n*100j, 0:1:n*100j]
        positions = np.vstack([xx.ravel(), yy.ravel()])
        values = np.vstack([xy.x, xy.y])
        kernel = st.gaussian_kde(values)
        f = np.reshape(kernel(positions).T, xx.shape)
        f = f / f.max() * 100

        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.plot_surface(xx, yy, f, cmap="Blues", lw=0.5, rstride=1, cstride=1)
        ax.view_init(elev=80., azim=-90)
        ax.contour(xx, yy, f, 10, colors="k", linestyles="solid")
        if show_save:
            plt.show()
        else:
            fig.savefig('C:/Users/User/Desktop/3d_plot.png')

        self.f = f

    def do_fs_beer(self):

        xy = self.xy
        
        fs = [[[k, v, j] for v, j in enumerate(i)]
            for k, i in enumerate(self.f)]
        fs = [i for i in fs if len(i) > 0]
        fs = reduce(lambda x, y: x + y, fs)
        fs = pd.DataFrame(fs, columns=['x', 'y','f'])
        fs = fs.sort_values('f',ascending=False)
        fs['l']=-1
        fs['l1']=-1
        fs[['x', 'y']]/=100

        Knn = KNeighborsClassifier(n_neighbors=1)
        Knn.fit(xy[['x','y']], xy.index)
        fs[['xx','yy']] = np.array(xy.loc[Knn.predict(fs[['x','y']]),['xx','yy']])
        fs.index = range(fs.shape[0])

        Knn = KNeighborsClassifier(n_neighbors=1)
        Knn.fit(fs[['x','y']], fs.index)
        lobl = Knn.predict(xy[['x','y']])
        unique, counts = np.unique(lobl, return_counts=True)

        fs['len'] = fs.index.map(dict(zip(unique, counts)))


        d_mat = pd.DataFrame(pairwise_distances(fs[['xx','yy']]))
        for i in range(d_mat.shape[0]):
            d_mat.iloc[i, i] = np.nan

        c = 100
        height = 5
        dbs = DBSCAN(eps= 0.015, min_samples=1)
        cl = []

        while c > 5:

            fs1 = fs.loc[fs.f > c - height]
            dbs = dbs.fit(fs1[['x', 'y']])
            fs.loc[fs1.index,'l'] = dbs.labels_

            a_get0 = fs.loc[fs1.index].groupby('l')['l1'].unique().reset_index()
            a_get0['l1'] = a_get0['l1'].map(lambda x: list(x))
            a_get0['1']=a_get0['l1'].map(lambda x: len([i for i in x if i!=-1 ]))
            a_get0 = list(itertools.chain(*a_get0.loc[a_get0['1'] >= 2, 'l1'].to_list()))
            a_get0 = [i for i in a_get0 if i != -1]
            a_get1 = fs.loc[fs1.index].groupby('l1')['l'].count()
            a_get1 = fs.loc[fs1.index].groupby('l1').apply(lambda x: pd.Series({
                'len': x['len'].sum(),
                'mind '+str(c): d_mat.loc[x.index, x.index].min().max() + 2 * d_mat.loc[x.index, x.index].min().std()
            }))

            a_get1 = a_get1.loc[a_get1['len']>50]
            a_get1 = a_get1.drop('len', axis=1)
            a_get1 = a_get1.loc[a_get1.index.isin(a_get0)]

            if len(a_get1) > 0:
                fs = fs.merge(a_get1, on = ['l1'], how = 'left')
                fs['col '+ str(c)] = np.nan
                fs.loc[fs['l1'].isin(a_get1.index),  'col ' + str(c)] = fs.loc[fs['l1'].isin(a_get1.index),'l1']

            fs['l1'] = copy.deepcopy(fs['l'])
            c -= height

        self.fs = fs



    def fs_regress_allneed(self):

        fs = self.fs

        d_framedata = fs.iloc[:,7:]
        col = d_framedata.columns
        d_framedata = d_framedata[[i for i in col if 'col' in i]]
        for i in range(0,d_framedata.shape[1]-1):
            re = list(d_framedata.iloc[:,i].dropna().index)

            for jj in range(i+1,d_framedata.shape[1]):

                a_var_step1 = list(d_framedata.iloc[re,jj].unique())
                promejutoc_var = d_framedata.iloc[:, jj]
                promejutoc_var[promejutoc_var.isin(a_var_step1)]=np.nan
                d_framedata.iloc[:, jj] = promejutoc_var


        col = d_framedata.columns
        def get_h_done(x):
            x_k = np.where(x >= 0)[0]
            if len(x_k)>0:
                k = min(list(x_k))
                res = [int(col[k].split(' ')[1]), x[k]]
            else:
                res = [np.nan]*2
            return res

        det_matrix = pd.DataFrame( np.array( d_framedata.apply(lambda x: get_h_done(x), axis =1).to_list()))
        fs = fs.join(det_matrix)
        fs['fin_join'] = det_matrix.astype(str).apply(lambda x: '-'.join(x), axis =1)
        fs = fs.sort_values([0,1])

        fs_to_plot = fs.loc[fs['fin_join']!='nan-nan']

        self.fs = fs
        self.fs_to_plot = fs_to_plot

        

    def do_color_cluster(self):

        fs_to_plot = self.fs_to_plot

        dist_mat_lil = get_inter_dist(fs_to_plot,'fin_join')
        fs_resullt = fs_to_plot.groupby([0,'fin_join'])['len'].sum().reset_index()

        print(dist_mat_lil)
        print(fs_resullt)

        num_dic={i:k for k,i in enumerate(fs_to_plot[0].unique())}

        dd= {}
        for i in range(len(fs_resullt)):

            dd_dicccy=list(dd.keys()) + list(dd.values())
            read_file = fs_resullt.loc[i,]
            idx = pd.IndexSlice
            d_ma = dist_mat_lil.loc[idx[:, read_file['fin_join']],:].dropna(1)
            d_ma = d_ma.sort_values(d_ma.index[0], axis =1).iloc[:,:4]
            print(d_ma)
            from_ = [i[1] for i in d_ma.columns if i[0]==read_file[0]]
            d_ma = d_ma.loc[:, idx[:,from_]]
            print(d_ma)
            
            if d_ma.shape[1]:
                ind = d_ma.columns[0][1]
                print(True)
            else:
                ind = read_file['fin_join'] 

            if read_file['fin_join'] not in dd_dicccy:
                dd[read_file['fin_join']] = ind

        print(dd)

        fs_to_plot['fin_join'] = fs_to_plot['fin_join'].map(dd)   ##
        
        self.fs_to_plot = fs_to_plot


    def do_model_clusterspare(self):

        fs_to_plot = self.fs_to_plot

        fs = self.fs
        
        fs = fs.drop(['fin_join'],axis=1).merge(fs_to_plot[['x','y','fin_join']], on = ['x','y'], how = 'left')
        llist = list(fs.loc[fs['fin_join'].isna()==False,0].unique()[::-1]) +[0.]
        fs[0] = fs['f'].map(lambda x: max([i for i in llist if i<= int(x)]))
        for i in llist:
            x = fs.loc[(fs[0]>=i)&(fs['fin_join'].isna()==False)]
            Knn = KNeighborsClassifier(n_neighbors=2)
            Knn.fit(x[['xx','yy']], x['fin_join'])
            print(i)
            if len(fs.loc[(fs[0]>=i)&(fs['fin_join'].isna()), 'fin_join']):
                fs.loc[(fs[0]>=i)&(fs['fin_join'].isna()), 'fin_join'] = Knn.predict(fs.loc[(fs[0]>=i)&(fs['fin_join'].isna()), ['xx','yy']])

        self.fs = fs


    def end(self):

        fs_to_plot = self.fs_to_plot

        xy = self.xy
           
        Knn = KNeighborsClassifier(n_neighbors=10)
        Knn.fit(fs_to_plot[['xx','yy']], fs_to_plot['fin_join'])
        xy[ 'fin_join'] = Knn.predict(xy[['xx','yy']])

        self.xy = xy


    def do_continious(self, xy, show_plots = True,
                      calc_aggregate_all= False,
                      percentile_cut = 10):

        if xy.shape[1] == 2:
            pass
        else:
            raise ValueError('A very specific bad thing happened.')

        if percentile_cut >= 0 and percentile_cut <= 100:
            pass
        else:
            raise ValueError('A very specific bad thing happened.')

        self.d3plot(xy, 1, show_save = True)
        self.do_fs_beer()
        self.fs_regress_allneed()
        plot_color_map(self.fs_to_plot[['x','y','fin_join']],
                       'first_exampl', show_save = True)

        if calc_aggregate_all:
            self.do_color_cluster()
            # aggregate clusters all
            plot_color_map(self.fs_to_plot[['x','y','fin_join']],
                       'second_exampl', show_save = True)

                
        self.do_model_clusterspare()

        fs = self.fs

        fs_to_plot = fs.loc[fs[0]>=percentile_cut]

        self.fs_to_plot = fs_to_plot

        plot_color_map(fs_to_plot[['x','y','fin_join']],
                       'third_exampl', show_save = True)

        self.end()
        
        plot_color_map(self.xy[['xx','yy','fin_join']],
                       'data_exampl', show_save = True)

    

if __name__ == '__main__':
    

    xy = pd.read_csv('C:/Users/User/Desktop/yyy.csv')[['lat','lon']]

    print(xy)

    xy['xx'], xy['yy'] = pyproj.transform(proj_wgs84, proj_gk4, xy['lon'].values,
                                                        xy['lat'].values)


    xy = xy[['xx', 'yy']]

    doubleclustering = Doubleclustering()

    doubleclustering.do_continious( xy, show_plots = True,
                        calc_aggregate_all= False,
                        percentile_cut = 10)


    fs_to_plot = doubleclustering.fs_to_plot

    fs_to_plot.to_excel(f'C:/Users/User/Desktop/res_gennu_result.xlsx')


    doubleclustering.xy[['xx','yy','fin_join']].to_csv('C:/Users/User/Desktop/yyknn_dus.csv')
