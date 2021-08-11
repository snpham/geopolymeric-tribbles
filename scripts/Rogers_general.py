# Data manipulation for CSCI 5502 Project
# Rogers

import numpy as np
from numpy.random import rand
import pandas as pd
import random
from pandas.io.parsers import read_csv
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import os                                                                                                #to check active working directory
import tkinter as tk
from random import randint
from tkinter import filedialog                                                                           #allow for dialog box file selection
from numpy.lib import corrcoef
from matplotlib.backends.backend_pdf import PdfPages                                                     #allow for save to PDF
from collections import Counter

cwd = os.getcwd()                                                                                        # Get the current working directory (cwd)
files = os.listdir(cwd)                                                                                  # Get all the files in that directory
print("Files in %r: %s" % (cwd, files))

#file = filedialog.askopenfilename(initialdir="/Users/kar3/Desktop/", title="Read Data")                 #select data file using dialog box

int_data = pd.read_feather('study_data/integrated_data.feather')                                         #read formatted data file with feather type
questions = np.array(pd.read_csv('study_data/project_survey_questions.csv'))                             #read .csv file containing questions corresponding to .feather headers

for i in range(0, len(questions)):
    print (str(i) +  ", Category: " + str(questions[i,0]) + ", Q: " + str(questions[i,1]))               #print the category of each question
    print("----------------------")                                                                      
    #questions_match = file[questions[i]]


def histAttribute(xpts,ypts):
    x_load = int_data[questions[xpts,0]].values                                                          #import the desire question for comparison to another and histogram plotting
    y_load = int_data[questions[ypts,0]].values

    df =pd.DataFrame(dict(                                                                               #combine two attributes in data frame to combine on histogram
    series=np.concatenate(([questions[xpts,0]]*len(x_load), [questions[ypts,0]]*len(y_load))),           #headers are category labels
    data  =np.concatenate((x_load,y_load))
    ))
    hist_data = px.histogram(df, x="data", color="series", barmode="overlay")                            #plot attribute vs each other
    
    hist_data.show()



def k_means(xpts, ypts,init_clust_type):
    x_load = int_data[questions[xpts,0]].values                                                          #import the desire question for comparison to another and histogram plotting
    y_load = int_data[questions[ypts,0]].values
    idx_list = []
    for idx,(i,j) in enumerate(zip(x_load,y_load)):
        if np.isnan(i) or np.isnan(j):
            idx_list.append(idx)
    x_loadx = np.delete(x_load,idx_list)
    y_loady = np.delete(y_load,idx_list)
    dfx = pd.DataFrame(x_loadx)
    dfy = pd.DataFrame(y_loady)
    pd.set_option('display.max_rows', None)                                                            #formatting for printing individual attribute values
    #dfy.to_csv('outputs/dfy.csv')                                                                     #only used for saving dataframes to search for nan values
    #dfx.to_csv('outputs/dfx.csv')

    # plt.rcParams["figure.figsize"] = (10,7)
    # plt.figure()                                                                                     #scatterplot init

    c = Counter(zip(x_loadx,y_loady))
    sizes = [c[(x1,y1)] for x1,y1 in zip(x_loadx,y_loady)]                                              #set the size of each point based on the number of occurences from all countries

    # plt.scatter(dfx,dfy, s=sizes, label=(str(questions[xpts,0]) + " and " + (questions[ypts,0])))     #print scatter plot of two attributes along with point sizes corresponding to magnitude of correspondence

    if init_clust_type == 0:                                                                            #0 corresponds to random initial clustering
        cluster_rand_index = np.random.uniform(low=1, high=5, size=10)                                   #the points for the inital clustering method, random
    elif init_clust_type == 1:                                                                          #1 corresponds to linear initial clusters
        cluster_rand_index = [1.1,2.1,3.5,4.1,4.7,1.3,2.2,3.2,4.3,4.8]                                                 #the points for the inital clustering method, linear
    cluster_rand_x = cluster_rand_index[0:5]
    cluster_rand_y = cluster_rand_index[5:10]
    cluster_rand_pts = [(x1,y1) for x1,y1 in zip(cluster_rand_x,cluster_rand_y)] 

    # plt.scatter(cluster_rand_x,cluster_rand_y, label="Initial clusters")                               #initial plot of clusters

    k_means_runs = 5        #--------NUMBER OF KMEANS ITERATIONS (including first cluster)--------------

    cluster_pts = [0]*k_means_runs
    cluster_pts[0] = cluster_rand_pts
    for i in range(0,k_means_runs-1):
        new_cluster_pts = cluster_process(cluster_pts[i],x_loadx,y_loady)                                #run initial k-means iteration with random start points
        # plt.scatter(new_cluster_pts[0],new_cluster_pts[1], label=("K means iteration " + str(i)))
        # plt.pause(0.0001)
        cluster_pts[i+1] = [(x1,y1) for x1,y1 in zip(new_cluster_pts[0],new_cluster_pts[1])]

    #run next iteration...
    #run until no change in array to cluster...
    

    # lgnd = plt.legend(bbox_to_anchor=(-.11, 1.1),loc='upper left')                                      #move legend outside of plot
    # lgnd.legendHandles[0]._sizes = [30]
    # lgnd.legendHandles[1]._sizes = [30]                                                                 #keep legend points same size, don't scale with "size" metric from scatter
    # plt.xlim(0.5, 5.5)
    # plt.ylim(0.5, 5.5)      #--------------change for DemAge and other 0-100 terms-------------------
    # plt.xlabel(questions[xpts,1])
    # plt.ylabel(questions[ypts,1])
    # plt.show()                                                                                          #plot every cluster until it converges
    return new_cluster_pts



def cluster_process(pts_to_cluster,x_load,y_load):
    point_counter = [0,0,0,0,0]
    array_counter_x = [0,0,0,0,0]
    array_counter_y = [0,0,0,0,0]                                                                           #define counters, will need to expand for more clusters
    new_cluster_x = [0,0,0,0,0]
    new_cluster_y = [0,0,0,0,0]
    for (i,j) in zip(x_load,y_load):
        man_dist_sum_int = []
        euc_dist_sum_int = []
        for k in pts_to_cluster:
            man_dist = (abs(i - k[0]) + abs(j-k[1]))                                                      #compute manhattan distance
            xy = np.array(i,j)
            euc_dist = np.linalg.norm(xy-k)                                                     #compute euclidean distance
            man_dist_sum_int.append(man_dist)
            euc_dist_sum_int.append(euc_dist)
        min_dist = np.argmin(euc_dist_sum_int)               #<---------change here for manhattan vs euclidean distance
        closest_clust= pts_to_cluster[min_dist]
        point_counter[min_dist] += 1
        array_counter_x[min_dist] += i
        array_counter_y[min_dist] += j
    for p in range(0,5):
        if point_counter[p] == 0:
            new_cluster_x[p],new_cluster_y[p] == pts_to_cluster[p]
            # new_cluster_y[p] == pts_to_cluster[p,1]
        else:
            new_cluster_x[p] = array_counter_x[p]/point_counter[p]
            new_cluster_y[p] = array_counter_y[p]/point_counter[p]
    #new_cluster_pts = [(x1,y1) for x1,y1 in zip(new_cluster_x,new_cluster_y)]
    return new_cluster_x,new_cluster_y                                                                  #return points in [xxx],[yyy] format for scatter plotting






    
if __name__ == '__main__':                                                                              #put attributes to compare here
    
    #histAttribute(20,7)
    
    #"Trust in Family" - very stable results as expected. Limited trust in family was uncommon, 
    # and when present paired with limited trust everywhere

    # for i in range(7,17):
    #     results = k_means(i,9,0)
    #     plt.scatter(results[0],results[1], label=("Attribute " + str(i)))

    # plt.xlabel("Trust in groups 2-13")
    # plt.ylabel("Trust in Other language speakers")
    # plt.show()
    #"Trust in other language speakers" - had more support as well for lower overall trust values

    #"Importance to do things for others" - also very stable results. More support for doing things 
    # for others than expected

    fig = go.Figure()
    for i in range(7,17):              # <-----------------WHO versus TRUST Section 1------------------
        results = k_means(i,68,1)
        fig.add_trace(go.Scatter(x=results[0],y=results[1], mode='markers',
                                text=questions[i,0], showlegend=False)) # hover text goes here)
        fig.update_layout(title='Information seen from WHO vs. Trust in all Groups',xaxis_title='Overall Trust',yaxis_title='Seen info from WHO? 1=Y, 2=N')
    df = pd.DataFrame(results)
    df.to_csv('/outputs/WHOvTrustTot.csv')
    fig.show()

    fig = go.Figure()
    for i in range(79,82):             # <-----------------WHO versus TRUST GOV section 2------------------
        results = k_means(i,68,1)
        fig.add_trace(go.Scatter(x=results[0],y=results[1], mode='markers',
                                text=questions[i,0], showlegend=False)) # hover text goes here)
        fig.update_layout(title='Information seen from WHO vs. Trust in Government',xaxis_title='Overall Gov. Trust',yaxis_title='Seen info from WHO? 1=Y, 2=N')
    df = pd.DataFrame(results)
    df.to_csv('/outputs/WHOvTrustGov.csv')
    fig.show()

    fig = go.Figure()
    for i in range(7,17):                # <--------------Estimates versus TRUST Section 1------------------
        results = k_means(i,92,0)
        fig.add_trace(go.Scatter(x=results[0],y=results[1], mode='markers',
                                text=questions[i,0], showlegend=False)) # hover text goes here)
        fig.update_layout(title='Certainty of Worldwide COVID Estimates vs. Trust in all Groups',xaxis_title='Overall Trust',yaxis_title='Belief in Estimates')
    df = pd.DataFrame(results)
    df.to_csv('/outputs/EstimatesvTrustTot.csv')
    fig.show()

#first classifier - those who lack in trust in general also lack trust in family?













#ii = np.where(a == 4)

#Notes
#add functionality where loads all headers and prints each with number identifier
    #can then select from various defined functions, run with different headers
#Apiori algorithm - implement as a function to compare two items based on input support value
    #could go from 25 to 2 data sets that satisfy suppport
    #partitioning out different categories can make this go quicker
#F-P tree construction - find frequent occurences in important itemsets, correlate with other sets in order of importance (i.e. f-c-a-b-m-p)
#Chi-squared correlation analysis for two attributes could be useful as well (pg. 267, lecture 6.d time 9:00)
#Look for negatively correlated items in survey (diet coke and coke in same order) (i.e. low trust in government, high trust in government spending or something)
    #this might help indicate outliers
#specify constraints in paper (rule constraints, dimension constraints likely)
#look at ordering data to establish monotonicity (if one satisfies, all do)
#use information gain to determine tree heirarchy, choose which attribute to cluster around
    #for 0<i<m, info(d) = -p*log_2(p)
    #gain = info(d)-info_attribute(d)
#implement accuracy, sensitivity, specificity, precision, recall for data set
    #use holdout method (2/3 training data, 1/3 test data) to establish good classifier to find above metrics (8.5, pg 371)
    #be sure to consider rule coverage and accuracy when generating rules for training data
#utilize backpropogation for data - use example in book, pg. 401
#clustering is grouping similar objects together without classification
#k means - establish random points, find distances, set clusters, move points to centers, reevaluate until convergence
#will need to divide our data into subspaces for simplified clustering (high dimensionality)
#need to choose a distance formula, or use both, for clustering
#write hierarchical clustering script that plots dendrogram?
#also attempt DBSCAN for density based clustering (for non 1-7 responses to questions)
# given we have high dimensionality, consider using biclusters or starting with subsets to determine correlation        
