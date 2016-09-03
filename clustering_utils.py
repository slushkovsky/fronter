import time
from math import sqrt, fabs
from enum import Enum
import random

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.metrics.pairwise import pairwise_distances_argmin
from sklearn.datasets.samples_generator import make_blobs

from assert_utils import *

class CLUST_MODE(Enum):
    K_MEANS = 1
    K_MINI_BATCH_MEANS = 2

PLOT_DEFAULT_BOUNDS = 10 #pixels


def example():
    '''
    This function is the example of clustering, which show differences 
    and similarities of KMeans and KMiniBatchKMeans methods.
    '''
    # Generate sample data
    np.random.seed(0)

    batch_size = 45
    centers = [[1, 1], [-1, -1], [1, -1]]
    n_clusters = len(centers)
    X, labels_true = make_blobs(n_samples=3000
                                    , centers=centers, cluster_std=0.7)

    # Compute clustering with Means
    k_means = KMeans(init='k-means++', n_clusters=3, n_init=10)
    t0 = time.time()
    k_means.fit(X)
    t_batch = time.time() - t0
    k_means_labels = k_means.labels_
    k_means_cluster_centers = k_means.cluster_centers_
    k_means_labels_unique = np.unique(k_means_labels)

    # Compute clustering with MiniBatchKMeans
    mbk = MiniBatchKMeans(init='k-means++', n_clusters=3,
                                    batch_size=batch_size, n_init=10,
                                    max_no_improvement=10, verbose=0)
    t0 = time.time()
    mbk.fit(X)
    t_mini_batch = time.time() - t0
    mbk_means_labels = mbk.labels_
    mbk_means_cluster_centers = mbk.cluster_centers_
    mbk_means_labels_unique = np.unique(mbk_means_labels)

    # Plot result
    fig = plt.figure(figsize=(8, 3))
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.05, top=0.9)
    colors = ['#4EACC5', '#FF9C34', '#4E9A06']

    order = pairwise_distances_argmin(k_means_cluster_centers,
                                      mbk_means_cluster_centers)
    # KMeans
    ax = fig.add_subplot(1, 3, 1)
    for k, col in zip(range(n_clusters), colors):
        my_members = k_means_labels == k
        cluster_center = k_means_cluster_centers[k]
        ax.plot(X[my_members, 0], X[my_members, 1], 'w',
                markerfacecolor=col, marker='.')
        ax.plot(cluster_center[0], cluster_center[1], 'o',
                                    markerfacecolor=col,
                                    markeredgecolor='k', markersize=6)
    ax.set_title('KMeans')
    ax.set_xticks(())
    ax.set_yticks(())
    plt.text(-3.5, 1.8,  'train time: %.2fs\ninertia: %f' % (
                                            t_batch, k_means.inertia_))

    # MiniBatchKMeans
    ax = fig.add_subplot(1, 3, 2)
    for k, col in zip(range(n_clusters), colors):
        my_members = mbk_means_labels == order[k]
        cluster_center = mbk_means_cluster_centers[order[k]]
        ax.plot(X[my_members, 0], X[my_members, 1], 'w',
                markerfacecolor=col, marker='.')
        ax.plot(cluster_center[0], cluster_center[1], 'o',
                                     markerfacecolor=col,
                                     markeredgecolor='k', markersize=6)
    ax.set_title('MiniBatchKMeans')
    ax.set_xticks(())
    ax.set_yticks(())
    plt.text(-3.5, 1.8, 'train time: %.2fs\ninertia: %f' %
                                        (t_mini_batch, mbk.inertia_))

    # Initialise the different array to all False
    different = (mbk_means_labels == 4)
    ax = fig.add_subplot(1, 3, 3)

    for l in range(n_clusters):
        different += ((k_means_labels == k) != \
                                        (mbk_means_labels == order[k]))

    identic = np.logical_not(different)
    ax.plot(X[identic, 0], X[identic, 1], 'w',
            markerfacecolor='#bbbbbb', marker='.')
    ax.plot(X[different, 0], X[different, 1], 'w',
            markerfacecolor='m', marker='.')
    ax.set_title('Difference')
    ax.set_xticks(())
    ax.set_yticks(())

    plt.show()

def mclust(data, n_clusters, mode=CLUST_MODE.K_MEANS):
    '''
    Allows to cluster the data into n_clusters, using two different
    modes.

    Parameters
    ----------
    @data        <list(Point)>  Data for clustering. 
    @n_clusters  <int>                     Nubmer of clusters.
    @mode        <class CLUST_MODE>        
    ----------
    Return       <list(int)>               List of labels for each point
    '''
    assert is_list_of(data, func=is_pixel)
    assert isinstance(n_clusters, int)
    assert isinstance(mode, CLUST_MODE)

    if mode == CLUST_MODE.K_MEANS:
        k_means = KMeans(init='k-means++', n_clusters=n_clusters, 
                                                              n_init=10)
        k_means.fit(data)
        labels = k_means.labels_
        cluster_centers = k_means.cluster_centers_

    if mode == CLUST_MODE.K_MINI_BATCH_MEANS:
        k_means = MiniBatchKMeans(init='k-means++', 
                                                  n_clusters=n_clusters)
        k_means.fit(data)
        labels = k_means.labels_
        cluster_centers = k_means.cluster_centers_
    
    return labels

def random_color():
    '''
    Return random-generated color in rgb.
    '''
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    return '#%02X%02X%02X' % (r, g, b)

def draw_clust(data, labels, name='plot'):
    '''
    This is the function that aims draw clustering on the plot.
    
    Parameters
    ----------
    @data     <list(Point)>   Clustered points. 
    @labels   <list(np.int32)>     List of clusters for each point.
    @name     <str>           Plot name          
    '''
    assert is_list_of(data, func=is_pixel)
    assert is_list_of(labels, need_type=np.int32)
    assert isinstance(name, str)
    assert len(labels) == len(data)

    colors = []
    
    fig = plt.figure()
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.05, top=0.9)
    ax = fig.add_subplot(1, 1, 1)
    
    for i in range(len(np.unique(labels))):
        colors.append(random_color())
    for i in range(len(data)):
        plt.plot(data[i][0], data[i][1], 'ro',
                                    markerfacecolor=colors[labels[i]])
    ax.set_title(name)
    ax.set_xticks(())
    ax.set_yticks(())
    
    plt.show()

def draw_double_clust(data1, labels1, data2, labels2):
    '''
    Shows two plots with custering in one window.
    Parameters
    ----------
    @data1     <list(Point)>   Clustered points. 
    @labels1   <list(int)>     List of clusters for each point.
    @data1     <list(Point)>   Clustered points. 
    @labels1   <list(int)>     List of clusters for each point.
    '''
    assert is_list_of(data1, is_pixel)
    assert is_list_of(labels1, int)
    assert labels1.size() == data1.size()
    
    assert is_list_of(data2, is_pixel)
    assert is_list_of(labels2, int)
    assert labels2.size() == data2.size()
    
    colors = []
    n_colors = max(len(np.unique(labels1)), len(np.unique(labels2)))
    for i in range(n_colors):
        colors.append(random_color())

    fig = plt.figure()
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.05, top=0.9)
    
    #PLOT 1
    ax = fig.add_subplot(1, 2, 1)
    for i in range(len(data1)):
        plt.plot(data1[i][0], data1[i][1], 'ro',
                                    markerfacecolor=colors[labels1[i]])
    ax.set_title('Data 1')
    ax.set_xticks(())
    ax.set_yticks(())
    
    #PLOT 2
    ax = fig.add_subplot(1, 2, 2)
    for i in range(len(data2)):
        plt.plot(data2[i][0], data2[i][1], 'ro',
                                    markerfacecolor=colors[labels2[i]])
    ax.set_title('Data 2')
    ax.set_xticks(())
    ax.set_yticks(())
   
    plt.show()
    

def dmatch_clust(kp1, kp2, match, count):
    '''
    Debug function, for clustering. This function transform mathed
    opencv.Keypoints to list of points, cluster it and show on the plot.
    ----------
    @kp1    <list(opencv.KeyPoint)>     Keypoints of the 1st image.
    @kp2    <list(opencv.KeyPoint)>     Keypoints of the 2nd image.
    @match  <list(opencv.DMatch)>       Matching
    @count  <int>                       Number of clusters
    '''
    assert isinstance(count, int)

    data = []
    for m in match:
        point1, point2 = kp1[m.queryIdx], kp2[m.trainIdx]
        x1, y1 = point1.pt 
        x2, y2 = point2.pt
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        data.append([fabs(x2 - x1), fabs(y2 - y1)])
    l = mclust(data, count)
    draw_clust(data, l, name='(|x2-x1|, |y2-y1|)')
