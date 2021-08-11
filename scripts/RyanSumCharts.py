import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
import sklearn.cluster as skl
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

firstDF = DF("integrated_dataNew.csv")

def scrubDF(df, keepList):
    df = df.drop(index=[0, 1, 2, 3])
    for col in df.columns:
        if col not in keepList:
            df = df.drop(col, axis=1)

    df1 = df.dropna()
    return df1

def graphCount(uncleandf, xAxis, yAxis, xName, yName, graphTitle):
    df = scrubDF(uncleandf, [xAxis,yAxis])
    s1 = df.groupby([xAxis,yAxis]).size()
    sumData = []
    for con, pol in zip(s1.index,s1):
        sumData.append([con[0], con[1], pol])
    newDF = pd.DataFrame(np.array(sumData), columns=[xName, yName, "Count"])
    newDF["Count"] = pd.to_numeric(newDF["Count"])

    fig = px.bar(newDF, x = xName, y = "Count", color=yName, title = graphTitle)
    fig.show()
    return newDF
       
plot1 = graphCount(firstDF, 'Residency', 'Politics', "Country", "Political Leaning (1-Conservative, 7-Liberal)", "Political Leaning by Country")
plot2 = graphCount(firstDF, 'Politics', 'Residency', "Political Leaning (1-Conservative, 7-Liberal)", "Country", "Political Leaning Breakdown")
plot3 = graphCount(firstDF, 'Politics', 'CanadaQ_1', "Political Affiliation (1-Conservative, 7-Liberal)", "Corona is a Serious Infection (1-Strongly Disagree, 5-Strongly Agree)", "Perceived Severity of Coronavirus by Political Affiliation")
plot4 = graphCount(firstDF, 'FinitePool_2', 'CanadaQ_1', "Personal Worry about Coronvirus", "Corona is a Serious Infection (1-Strongly Disagree, 5-Strongly Agree)", "Worry about Corona and Perceived Severity")
