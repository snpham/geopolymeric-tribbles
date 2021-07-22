# Data manipulation for CSCI 5502 Project
# Rogers

import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import os                                                                                                #to check active working directory
import tkinter as tk
from tkinter import filedialog                                                                           #allow for dialog box file selection
from numpy.lib import corrcoef
from matplotlib.backends.backend_pdf import PdfPages                                                     #allow for save to PDF

cwd = os.getcwd()                                                                                        # Get the current working directory (cwd)
files = os.listdir(cwd)                                                                                  # Get all the files in that directory
print("Files in %r: %s" % (cwd, files))

#file = filedialog.askopenfilename(initialdir="/Users/kar3/Desktop/", title="Read Data")                 #select data file using dialog box

int_data = np.array(pd.read_feather('study_data/integrated_data.feather'))                               #read formatted data file with feather type
questions = np.array(pd.read_csv('study_data/project_survey_questions.csv'))                             #read .csv file containing questions corresponding to .feather headers

for i in range(0, len(questions)):
    print (str(i) +  ", Category: " + str(questions[i,0]) + ", Q: " + str(questions[i,1]))               #print the category of each question
    print("----------------------")                                                                      
    #questions_match = file[questions[i]]



def histAttribute(xpts,ypts):
    x_load = int_data[xpts]                                                                              #import the desire question for comparison to another and histogram plotting
    y_load = int_data[ypts]

    df =pd.DataFrame(dict(                                                                               #combine two attributes in data frame to combine on histogram
    series=np.concatenate(([questions[xpts,0]]*len(x_load), [questions[ypts,0]]*len(y_load))),           #headers are category labels
    data  =np.concatenate((x_load,y_load))
    ))
    hist_data = px.histogram(df, x="data", color="series", barmode="overlay")                            #plot attribute vs each other
    
    hist_data.show()



def k_means(xpts, ypts):
    x_load = int_data[xpts]                                                                              #import the desire question for comparison to another and histogram plotting
    y_load = int_data[ypts]

    plt.figure()
    plt.scatter(x_load,y_load, label=(str(questions[xpts,0]) + "and" + (questions[ypts,0])))

    cluster_rand_init = [int_data[22],int_data[37],int_data[56]]                                        #the points for the inital clustering method
    cluster_rand_pts = np.vstack(cluster_rand_init)                                                     #organize points in np.array
   
    xpt_clust = cluster_rand_pts[:,0].tolist()
    ypt_clust = cluster_rand_pts[:,1].tolist()  

    plt.scatter(xpt_clust,ypt_clust, label="Initial clusters")
    cluster_process(cluster_rand_pts)
    #run next iteration...
    #run until no change in array to cluster...

    plt.legend()
    plt.show()                                                                                          #plot every cluster until it converges

def cluster_process(pts_to_cluster):
    point_counter = []
    for i in int_data:
        man_dist_sum_int = []
        for j in pts_to_cluster:
            man_dist = abs(i - j)
            man_dist_sum = man_dist[0]+man_dist[1]                                                      #compute manhattan distance
            man_dist_sum_int.append(man_dist_sum)
        print("Manhattan distances for point " + str(i) + " = " + str(man_dist_sum_int))
        min_dist = np.argmin(man_dist_sum_int)
        closest_clust= pts_to_cluster[min_dist]
        print("Closest initial cluster is " + str(closest_clust))
        #then add together each point that is in each cluster...
        #output as new array to use for next iteration...






    
if __name__ == '__main__':                                                                              #put attributes to compare here
    
    histAttribute(6,7)
    
    k_means(6,7)













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
