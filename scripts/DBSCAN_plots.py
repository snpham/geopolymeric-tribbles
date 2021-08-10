import pandas as pd
import numpy as np
import os
import plotly.express as px

# cwd = os.getcwd()

info_results = pd.read_feather('scripts/cluster_results/info.feather')

SocialmediatrustQ1 = px.scatter(info_results, x="SocialmediatrustQ1", y="CanadaQ_1", color="labels",
                 size='WHOtrustQ1', labels=dict(CanadaQ_1="Susceptibility to Misinformation (1 is most susceptible)",
                                                SocialmediatrustQ1="Trust in social media (7 is complete trust)"),
                 title='<b>Results of DBSCAN clustering based on trust in information sources</b><br>\
                        Epsilon = 1, Attributes : Canada_Q1, SocialmediatrustQ1,journalisttrustQ1,FriendstrustQ1,WHOtrustQ1<br>\
                        ')
# SocialmediatrustQ1.show()

politics_results = pd.read_feather('scripts/cluster_results/politics.feather')

Politics = px.scatter(politics_results, x="Politics", y="labels", color="labels",
                 labels=dict(labels="Assigned cluster label",
                             Politics="Politics (1 very left, 7 very right)"),
                 title='<b>Results of DBSCAN clustering based on trust in information sources</b><br>\
                        Epsilon = 1, Attributes :CanadaQ_1, Politics, prosocial, CultCog_1, CultCog_2,CultCog_3<br>\
                        Susceptible individuals are in clusters 2 and 7, all others are less susceptible')
# Politics.show()