import pandas as pd
import numpy as np
import os
from math import *
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
import plotly.express as px

save_data_for_plots=True # set to True to save results of clustering for visualizations
df = pd.read_feather("integrated_data.feather")
## eps = 0.5 ==> 5903 are "noise"
def DBSCAN_results(epsilon, attributes, df=df):
    attr_df = df[attributes]
    # attr_df = attr_df.loc[~(attr_df.CanadaQ_1.isnull())]
    # for now, drop all nulls. maybe replace with a neutral/mean later?
    attr_df = attr_df.dropna()
    print("Individuals included after null values dropped: {}".format(len(attr_df)))
    X = attr_df.to_numpy()
    X = StandardScaler().fit_transform(X)
    db = DBSCAN(eps=epsilon, min_samples=10).fit(X)
    # core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    # core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_  # -1 is
    count = np.count_nonzero(labels == -1)
    print("{} considered noise".format(count))
    n_clusters_ = np.max(labels)
    print("{} estimated clusters".format(n_clusters_+1))
    return attr_df, db

cwd = os.getcwd()

corr=pd.read_csv("FullCorrelations.csv")
corr.set_index('Unnamed: 0', inplace=True)

df = pd.read_feather("integrated_data.feather")
# run clustering without countries, map clusters back to countries in post-processing

attributes = ['CanadaQ_1', 'MediaExp_2', 'MediaExp_3', 'MediaExp_4', 'MediaExp_5',
              'MediaExp_6', 'MediaExp_7', 'SocialmediatrustQ1', 'journalisttrustQ1',
              'govtrustQ1', 'FriendstrustQ1', 'WHOtrustQ1']

def get_correlations(attributes):
    corr_attr=corr[attributes]
    corr_attr=corr_attr.loc[corr_attr.index.isin(attributes)]
    for col in corr_attr.columns:
        correlated_with = list(corr_attr.loc[corr_attr[col]>0.3][col].index)
        for i in correlated_with:
            if i != col:
                r = corr_attr.loc[corr_attr[col] > 0.3][col].loc[i]
                print("{} is correlated with {} (corr = {:.3f})".format(col, i, r))
    return corr_attr


def look_at_results(attributes_df, db):
    labels = db.labels_  # -1 is noise
    count = np.count_nonzero(labels == -1)

    attributes_df = attributes_df.assign(labels=labels)
    no_noise = attributes_df.loc[attributes_df.labels > -1]
    print("Individuals included without noise labels: {}".format(len(no_noise)))
    vsus = attributes_df.loc[attributes_df.CanadaQ_1 < 2]
    print("Very susceptible individuals in clusters:", end=' ')
    print(vsus.labels.unique())
    sus = attributes_df.loc[attributes_df.CanadaQ_1 == 2]
    print("Susceptible individuals in clusters:", end=' ')
    print(sus.labels.unique())
    n_sus = attributes_df.loc[attributes_df.CanadaQ_1 >= 3]
    n_sus.labels.unique()
    print("Less susceptible individuals in clusters:", end=' ')
    print(n_sus.labels.unique())
    return attributes_df

new_attributes=['CanadaQ_1', 'SocialmediatrustQ1', 'journalisttrustQ1',
                 'FriendstrustQ1', 'WHOtrustQ1']

# check for correlated attributes
corr_attr = get_correlations(new_attributes)
# perform clustering
info, db = DBSCAN_results(1, new_attributes)
# map label back to objects
info = look_at_results(info, db)

# visualize
no_noise = info.loc[info.labels > -1]
if save_data_for_plots == True:
    no_noise.reset_index().to_feather(cwd+"\\cluster_results\\info.feather")
    info.reset_index().to_feather(cwd+"\\cluster_results\\info_w_noise.feather")

fig = px.scatter(no_noise, x="SocialmediatrustQ1", y="CanadaQ_1", color="labels",
                 size='WHOtrustQ1', title='<b>Results of DBSCAN clustering based on trust in information sources</b><br>\
                                          Epsilon = 1, Attributes : Canada_Q1, SocialmediatrustQ1,journalisttrustQ1,FriendstrustQ1,WHOtrustQ1')
fig.show()

# fig.write_image(cwd+'/project_images/DBSCAN_info_source_eps1.png')

#Got rid of CultCog_5 and  'CultCog_4' CultCog_6
new_attributes=['CanadaQ_1','Politics', 'prosocial', 'CultCog_1', 'CultCog_2',
                'CultCog_3',]

# check for correlated attributes
corr_attr = get_correlations(new_attributes)
# perform clustering
politics, db = DBSCAN_results(1, new_attributes)# map label back to objects
politics = look_at_results(politics, db)

# identify clusters by "susceptibility"
vsus = politics.loc[politics.CanadaQ_1 < 2]
print("Very susceptible individuals in clusters:", end=' ')
print(vsus.labels.unique())
sus = politics.loc[politics.CanadaQ_1 == 2 ]
print("Susceptible individuals in clusters:", end=' ')
print(sus.labels.unique())
n_sus = politics.loc[politics.CanadaQ_1 >= 3]
n_sus.labels.unique()
print("Less susceptible individuals in clusters:", end=' ')
print(n_sus.labels.unique())

# visualize
no_noise = politics.loc[politics.labels > -1]

if save_data_for_plots == True:
    no_noise.reset_index().to_feather(cwd+"\\cluster_results\\politics.feather")
    politics.reset_index().to_feather(cwd+"\\cluster_results\\politics_w_noise.feather")

fig = px.scatter(no_noise, x="Politics", y="labels", #"CanadaQ_1", color="",
                 size='prosocial')
fig.show()

"""look at trends in each cluster"""
import plotly.graph_objects as go

politics_results = pd.read_feather(cwd + "\\cluster_results\\politics_w_noise.feather")
for cluster in politics_results.labels.unique():
    cluster_df=politics_results.loc[politics_results.labels==cluster]
    del cluster_df['index']
    fig = go.Figure()
    for attribute in cluster_df.columns:
        if attribute != 'labels':
            fig.add_trace(go.Box(y=cluster_df[attribute].values,
                                 name=attribute,))
    fig.update_layout(title_text="Cluster {}: Attribute distributions".format(cluster))
    fig.show()

info_results = pd.read_feather(cwd + "\\cluster_results\\info_w_noise.feather")

vsus = info_results.loc[info_results.CanadaQ_1 < 2]
print("Very susceptible individuals in clusters:", end=' ')
print(vsus.labels.unique())
sus = info_results.loc[info_results.CanadaQ_1 == 2 ]
print("Susceptible individuals in clusters:", end=' ')
print(sus.labels.unique())
n_sus = info_results.loc[info_results.CanadaQ_1 >= 3]
n_sus.labels.unique()
print("Less susceptible individuals in clusters:", end=' ')
print(n_sus.labels.unique())

for cluster in info_results.labels.unique():
    cluster_df=info_results.loc[info_results.labels==cluster]
    del cluster_df['index']
    fig = go.Figure()
    for attribute in cluster_df.columns:
        if attribute != 'labels':
            fig.add_trace(go.Box(y=cluster_df[attribute].values,
                                 name=attribute,))
    fig.update_layout(title_text="Cluster {}: Attribute distributions".format(cluster))
    fig.show()
"""Attempt to visualize clusters by separating individuals with distance measures"""
def distance_from_center(row, comparison_vector):
    x = []
    for col in new_attributes:
        x.append(row[col])
    return sqrt(sum((a-b)**2 for a,b in zip(x,comparison_vector)))
#experiment w visualizations
mins=[]
medians=[]
for col in new_attributes:
    mins.append(politics[col].min())
    medians.append(politics[col].median())
politics['distance_from_min']=politics.apply(distance_from_center, args=[mins], axis=1)
politics['distance_from_median']=politics.apply(distance_from_center, args=[medians], axis=1)

no_noise = politics.loc[politics.labels > -1]
fig = px.scatter(no_noise, x="CanadaQ_1", y="distance_from_min", color="labels",
                 size='prosocial')
fig.show()
fig = px.scatter(no_noise, x="distance_from_median", y="distance_from_min", color="labels",)
                 #size='prosocial')
fig.show()

""""""
# # cluster only susceptible
# new_attributes=['Politics', 'prosocial', 'CultCog_1', 'CultCog_2',
#                 'CultCog_3','SocialmediatrustQ1', 'journalisttrustQ1', 'WHOtrustQ1']#, 'Trustingroups_7', 'Trustingroups_9', 'Trustingroups_10', 'Trustingroups_12',]
#
# # check for correlated attributes
# corr_attr = get_correlations(new_attributes)
# # perform clustering
# politics, db = DBSCAN_results(5, new_attributes, df=df.loc[df.CanadaQ_1<3])# map label back to objects
# #cant get good clusters :/
# politics = look_at_results(politics, db)
