import pandas as pd
import numpy as np
import plotly.express as px

firstDF = pd.read_csv('outputs/integrated_dataNew.csv', dtype=str)
colors = {
    'background': '#3D405B',
    'text': '#fbfbfc'
}

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
    fig.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'],
        font_color=colors['text'])
    # fig.show()
    return fig
       
plot1 = graphCount(firstDF, 'Residency', 'Politics', "Country", "Political Leaning (1-Liberal, 7-Conservative)", "Political Leaning by Country")
plot2 = graphCount(firstDF, 'Politics', 'Residency', "Political Leaning (1-Liberal, 7-Conservative)", "Country", "Political Leaning Breakdown")
plot3 = graphCount(firstDF, 'Politics', 'CanadaQ_1', "Political Affiliation (1-Liberal, 7-Conservative)", "Corona is a Serious Infection (1-Strongly Disagree, 5-Strongly Agree)", "Perceived Severity of Coronavirus by Political Affiliation")
plot4 = graphCount(firstDF, 'FinitePool_2', 'CanadaQ_1', "Personal Worry about Coronvirus", "Corona is a Serious Infection (1-Strongly Disagree, 5-Strongly Agree)", "Worry about Corona and Perceived Severity")
