# Kmeans plotting for vizualizations
# Rogers

import numpy as np
import pandas as pd
from pandas.io.parsers import read_csv
import plotly.express as px
import plotly.graph_objects as go


int_data = pd.read_feather('study_data/integrated_data.feather')                                         #read formatted data file with feather type
questions = np.array(pd.read_csv('study_data/project_survey_questions.csv'))

# -----------------WHO versus TRUST Section 1------------------
results = np.array(pd.read_csv('outputs/WHOvTrustTot.csv', converters={'0': eval, '1':eval}))

fig = go.Figure()
for i in range (0,len(results)):
    fig.add_trace(go.Scatter(x=results[i,1],y=results[i,2], mode='markers',
                        text=questions[i+6,1], showlegend=False)) # hover text goes here)
    fig.update_layout(title='Information seen from WHO vs. Trust in all Groups',xaxis_title='Overall Trust',yaxis_title='Seen info from WHO? 1=Yes, 2=No')
    fig.update_traces(marker_size=10)
fig.show()

# -----------------WHO versus TRUST GOV section 2------------------
results = np.array(pd.read_csv('outputs/WHOvTrustGov.csv', converters={'0': eval, '1':eval}))

fig = go.Figure()
for i in range (0,len(results)):
    fig.add_trace(go.Scatter(x=results[i,1],y=results[i,2], mode='markers',
                        text=questions[i+78,1], showlegend=False)) # hover text goes here)
    fig.update_layout(title='Information seen from WHO vs. Trust in Government',xaxis_title='Trust in Government',yaxis_title='Seen info from WHO? 1=Yes, 2=No')
    fig.update_traces(marker_size=10)
fig.show()

# --------------Estimates versus TRUST Section 1------------------
results = np.array(pd.read_csv('outputs/EstimatesvTrustTot.csv', converters={'0': eval, '1':eval}))

fig = go.Figure()
for i in range (0,len(results)):
    fig.add_trace(go.Scatter(x=results[i,1],y=results[i,2], mode='markers',
                        text=questions[i+6,1], showlegend=False)) # hover text goes here)
    fig.update_layout(title='Certainty of Worldwide COVID Estimates vs. Trust in all Groups',xaxis_title='Overall Trust',yaxis_title='Belief in Estimates')
    fig.update_traces(marker_size=10)
fig.show()

# --------------Worry versus Affected Level------------------
results = np.array(pd.read_csv('outputs/WorryvAffected.csv', converters={'0': eval, '1':eval}))

fig = go.Figure()
for i in range (0,len(results)):
    fig.add_trace(go.Scatter(x=results[i,1],y=results[i,2], mode='markers',
                        text=questions[i+20,1], showlegend=False)) # hover text goes here)
    fig.update_layout(title='Worry about COVID vs. Affected from COVID',xaxis_title='Overall Affected Level',yaxis_title='Worry Level')
    fig.update_traces(marker_size=10)
fig.show()

# --------------Social Media use versus Affected level------------------
results = np.array(pd.read_csv('outputs/SocialvAffected.csv', converters={'0': eval, '1':eval}))

fig = go.Figure()
for i in range (0,len(results)):
    fig.add_trace(go.Scatter(x=results[i,1],y=results[i,2], mode='markers',
                        text=questions[i+20,1], showlegend=False)) # hover text goes here)
    fig.update_layout(title='Social Media Use vs. Affected from COVID',xaxis_title='Overall Affected level',yaxis_title='Social Media Usage? 1=Yes, 2=No')
    fig.update_traces(marker_size=10)
fig.show()
