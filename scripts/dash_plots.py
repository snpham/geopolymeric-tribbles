import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
from scripts.frequents import apriori
from scripts.DBSCAN_plots import *

savefigs = False


## project - frequent itemsets
dataset = pd.read_csv(r'https://raw.githubusercontent.com/summeryriddles/geopolymeric-tribbles/main/study_data/integrated_data_v3.csv', 
                      index_col=0, header=0)
dataset_prep = dataset[['prep']].dropna()
dataset_prep = dataset_prep[~dataset_prep.prep.str.contains("E+")]
dataset_country = dataset[['Residency','prep']].dropna()
dataset_country = dataset_country[~dataset_country.prep.str.contains("E+")]

df_meta = pd.read_csv(r'https://raw.githubusercontent.com/summeryriddles/geopolymeric-tribbles/main/study_data/metadata.csv', index_col=0, 
                        header=None, usecols=range(1,4), encoding='latin1')

colors = {
    'background': '#3D405B',
    'text': '#fbfbfc'
}

## table of preparation activities
prep_dict = {}
for val in df_meta.loc['prep', 3].strip().split(','):
    val = val.split('=')
    prep_dict[val[0].strip()] = val[1].strip()
df_meta_desc = pd.DataFrame.from_dict(prep_dict, orient='index', 
                                      columns=['Description'])
activity_table = go.Figure(data=[go.Table(columnwidth=[1, 4],
                           header=dict(values=['Activity', 'Description']),
                           cells=dict(values=[list(prep_dict.keys()),
                                              list(prep_dict.values())]))])
if savefigs:
    pass
else:
    activity_table.update_layout(plot_bgcolor=colors['background'],
                                paper_bgcolor=colors['background'])


if savefigs:
    update_layout_colorful = dict(barmode='relative', 
        xaxis=dict(title='activity',titlefont_size=16,tickfont_size=14, type='category'),
        yaxis=dict(title='support',titlefont_size=16,tickfont_size=14),
        hovermode="x unified")
else:
    update_layout_colorful = dict(barmode='relative', 
        xaxis=dict(title='activity',titlefont_size=16,tickfont_size=14, type='category'),
        yaxis=dict(title='support',titlefont_size=16,tickfont_size=14),
        plot_bgcolor=colors['background'], paper_bgcolor=colors['background'],
        font_color=colors['text'], hovermode="x unified")


## graph 1 ##
# get all countries with frequent-set 1
countries = ['US', 'CN', 'AU', 'DE', 'ES', 'IT', 'JP', 'KR', 'MX', 'UK', 'SE']
df_countries = []
minsup_countries = []
scans1_countries = []
scans2_countries = []
scans3_countries = []
gobars = []
min_sup = 0.01
count3 = 0
for ii, country in enumerate(countries):
    df_country = dataset_country[dataset_country['Residency'] == country]
    minsup_country = min_sup * len(df_country)
    df_country = df_country.drop('Residency', axis=1)
    # scans1_country, _, _ = apriori(df_country, minsup_country)
    # if count3 == 0:
    #     dfscan_country = pd.DataFrame(scans1_country.items(), columns=['activity', country])
    #     count3 +=1
    # else:
    #     dfscan_country[country] = scans1_country.values()
    # dfscan_country.to_csv('outputs/df_freq1_by_countries.csv')
    scan1 = pd.read_csv('outputs/df_freq1_by_countries.csv')
    scans1_country = dict(zip(scan1.loc[:,'activity'], scan1.loc[:,country]))
    scans1_country = {key:value/len(df_country) for (key, value) in scans1_country.items()}
    gobars.append(go.Bar(name=country, x=list(scans1_country.keys()), 
                         y=list(scans1_country.values()), base=0))
Support_AllCountries = go.Figure(data=gobars[:])
Support_AllCountries.update_layout(title=f'Support of Preparation Activities, by Country <br>'
                                         f'          - frequentset-1. min support: {min_sup}')
# Change the bar mode
Support_AllCountries.update_layout(update_layout_colorful)

# scan1 = pd.read_csv('outputs/df_freq1_by_countries.csv', index_col=0)
# dfscan_country = scan1.sort_values(by=['activity'], ascending=True)
# dfscan_country.to_csv('outputs/df_freq1_by_countries.csv')


## graph 2 ##
if savefigs:
    update_layout = dict(barmode='group',
                        yaxis=dict( titlefont_size=16, tickfont_size=16),
                        xaxis=dict( tickangle=-45, titlefont_size=16, tickfont_size=16, type='category'),
                        hoverlabel=dict(font_size=14))
    update_traces = dict(marker_line_width=1.5, opacity=0.7)
else:
    update_layout = dict(barmode='group',
                yaxis=dict( titlefont_size=16, tickfont_size=16),
                xaxis=dict( tickangle=-45, titlefont_size=16, tickfont_size=16, type='category'),
                plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],
                font_color=colors['text'], hoverlabel=dict(font_size=14))
    update_traces = dict(marker_color='#a0a4c0', marker_line_color='#52567A',
                        marker_line_width=1.5, opacity=0.7)


# get global frequentset-1
min_sup = 0.01
min_sup *= len(dataset_prep)
# scan1, _, _ = apriori(dataset_prep, min_sup)
# df_scan1 = pd.DataFrame(data=scan1.items(), index=None, columns=['activity', 'value']).astype('int')
# df_scan1 = df_scan1.sort_values(by=['activity'], ascending=True)
# df_scan1.to_csv('outputs/df_001sup_freq1.csv')
scan1 = pd.read_csv('outputs/df_001sup_freq1.csv', index_col=0)
scan1 = dict(zip(scan1.iloc[:,0], scan1.iloc[:,1]))

prep_merged = {key:value/len(dataset_prep) for (key, value) in scan1.items()}
prep_merged = pd.DataFrame.from_dict(prep_merged, orient='index', 
                                     columns=['support'])
freqset_1 = px.bar(prep_merged, y='support', x=prep_merged.index, 
                   labels={'index': 'activity'})
freqset_1.update_layout(title=f'Support of Preparation Activities, Global <br>'
                f'          - frequentset-1. min support: {min_sup/len(dataset_prep)}')
freqset_1.update_traces(update_traces)
freqset_1.update_layout(dict(yaxis=dict(range=[0, 1])))
freqset_1.update_layout(update_layout)


## graph 3 ##
# increase support and view higher frequentsets (2 and 3)
min_sup = 0.5
min_sup *= len(dataset_prep)
# _, scan2, scan3 = apriori(dataset_prep, min_sup)
# df_scan2 = pd.DataFrame(data=scan2.values(), index=scan2.keys())
# df_scan3 = pd.DataFrame(data=scan3.values(), index=scan3.keys())
# df_scan2.to_csv('outputs/df_05sup_freq2.csv')
# df_scan3.to_csv('outputs/df_05sup_freq3.csv')
scan2 = pd.read_csv('outputs/df_05sup_freq2.csv')
scan3 = pd.read_csv('outputs/df_05sup_freq3.csv')
scan2 = dict(zip(scan2.iloc[:,0], scan2.iloc[:,1]))
scan3 = dict(zip(scan3.iloc[:,0], scan3.iloc[:,1]))

prep2 =  {key:value/len(dataset_prep) for (key, value) in scan2.items()}
prep2_supp = pd.DataFrame.from_dict(prep2, orient='index', 
                                    columns=['support'])
freqset_2 = px.bar(prep2_supp, x=prep2_supp.index, y='support', 
                   labels={'index': 'activities'})
freqset_2.update_traces(update_traces)
freqset_2.update_layout(update_layout)
freqset_2.update_layout(dict(yaxis=dict(range=[0.4, 0.9])))
freqset_2.update_layout(title=f'Support of Preparation Activities, Global <br>'
                f'          - frequentset-2. min support: {min_sup/len(dataset_prep)}')


## graph 4 ##
prep3 =  {key:value/len(dataset_prep) for (key, value) in scan3.items()}
prep3_supp = pd.DataFrame.from_dict(prep3, orient='index', 
                                    columns=['support'])
freqset_3 = px.bar(prep3_supp, x=prep3_supp.index, y='support', 
                  labels={'index': 'activities'})
freqset_3.update_traces(update_traces)
freqset_3.update_layout(update_layout)
freqset_3.update_layout(dict(yaxis=dict(range=[0.4, 0.9])))
freqset_3.update_layout(title=f'Support of Preparation Activities, Global <br>'
                f'          - frequentset-3. min support: {min_sup/len(dataset_prep)}')


## bayesian classifications
if savefigs:
    update_layout_colorful = dict(barmode='relative', 
        xaxis=dict(title='Country',titlefont_size=16,tickfont_size=14),
        yaxis=dict(title='P(Ci)',titlefont_size=16,tickfont_size=14),
        hovermode="x unified")
else:
    update_layout_colorful = dict(barmode='relative', 
        xaxis=dict(title='Country',titlefont_size=16,tickfont_size=14),
        yaxis=dict(title='P(Ci)',titlefont_size=16,tickfont_size=14),
        plot_bgcolor=colors['background'], paper_bgcolor=colors['background'],
        font_color=colors['text'], hovermode="x unified")
# graph 4
dataset = pd.read_csv('outputs/naive_bayesian_vaccine_global.csv', index_col=0, header=0)
bayes_vaccine_global = go.Figure(data=[
    go.Bar(name='Recommend-Yes', x=dataset['Residency'].unique(), 
                        y=dataset['Recommend-Yes'], base=0),
    go.Bar(name='Vaccine-Yes', x=dataset['Residency'].unique(), 
                         y=dataset['Vaccine-Yes'], base=0),
    go.Bar(name='Vaccine-No', x=dataset['Residency'].unique(), 
                         y=dataset['Vaccine-No'], base=0),
    go.Bar(name='Recommend-No', x=dataset['Residency'].unique(), 
                         y=dataset['Recommend-No'], base=0),
                         ])
bayes_vaccine_global.update_layout(title="Probability of Vaccination and Recommending, by Country")
bayes_vaccine_global.update_traces(dict(marker_line_width=1.5, opacity=0.7))
bayes_vaccine_global.update_layout(update_layout_colorful)
# bayes_vaccine_global.show()

if savefigs:
    update_layout_colorful = dict(barmode='relative', 
        xaxis=dict(title='Age Group',titlefont_size=16,tickfont_size=14),
        yaxis=dict(title='P(X|Ci)P(Ci)',titlefont_size=16,tickfont_size=14),
        hovermode="x unified")
else:
    update_layout_colorful = dict(barmode='relative', 
        xaxis=dict(title='Age Group',titlefont_size=16,tickfont_size=14),
        yaxis=dict(title='P(X|Ci)P(Ci)',titlefont_size=16,tickfont_size=14),
        plot_bgcolor=colors['background'], paper_bgcolor=colors['background'],
        font_color=colors['text'], hovermode="x unified")
# graph 5
dataset = pd.read_csv('outputs/naive_bayesian_vaccine_age_global.csv', index_col=0, header=0)
naive_bayesian_vaccine_age_global = go.Figure(data=[
    go.Bar(name='Recommend-Yes, by Age', x=dataset['age_range'].unique(), 
                         y=dataset['Recommend-Yes, by Age'], base=0),
    go.Bar(name='Vaccine-Yes, by Age', x=dataset['age_range'].unique(), 
                         y=dataset['Vaccine-Yes, by Age'], base=0),
    go.Bar(name='Vaccine-No, by Age', x=dataset['age_range'].unique(), 
                         y=dataset['Vaccine-No, by Age'], base=0),
    go.Bar(name='Recommend-No, by Age', x=dataset['age_range'].unique(), 
                         y=dataset['Recommend-No, by Age'], base=0),
                         ])
naive_bayesian_vaccine_age_global.update_layout(title="Naive Bayesian Probability Global, by Age Group")
naive_bayesian_vaccine_age_global.update_traces(dict(marker_line_width=1.5, opacity=0.7))
naive_bayesian_vaccine_age_global.update_layout(update_layout_colorful)
# naive_bayesian_vaccine_age_global.show()

# graph 6
dataset = pd.read_csv('outputs/naive_bayesian_canada1_global.csv', index_col=0, header=0)
naive_bayesian_canadaq1_age_global = go.Figure(data=
    [go.Bar(name='Serious-Yes Probability', x=dataset['age_range'].unique(), 
                         y=dataset['Serious-Yes Probability'], base=0),
    go.Bar(name='Serious-No Probability', x=dataset['age_range'].unique(), 
                         y=dataset['Serious-No Probability'], base=0),
                         ])
naive_bayesian_canadaq1_age_global.update_layout(title="Naive Bayesian - CanadaQ1, by Age Group")
naive_bayesian_canadaq1_age_global.update_traces(dict(marker_line_width=1.5, opacity=0.7))
naive_bayesian_canadaq1_age_global.update_layout(update_layout_colorful)
# naive_bayesian_canadaq1_age_global.show()

numerical_dataset = pd.read_csv('outputs/numerical_dataset.csv')
num1_stats = px.box(numerical_dataset, x="Residency", y="Num1", notched=True, points='all')
num1_stats.add_shape(type='line', x0='AU',y0=0.25,x1='US',y1=0.25,
                line=dict(color='Red',), xref='x', yref='y')
# num1_stats.show()
num2_stats = px.box(numerical_dataset, x="Residency", y="Num2a", notched=True, points='all')
num2_stats.add_shape(type='line', x0='AU',y0=0.6,x1='US',y1=0.6,
                line=dict(color='Red',), xref='x', yref='y')
# num2_stats.show()
num3_stats = px.box(numerical_dataset, x="Residency", y="Num2b", notched=True, points='all')
num3_stats.add_shape(type='line', x0='AU',y0=0.285714,x1='US',y1=0.285714,
                line=dict(color='Red',), xref='x', yref='y')
# num3_stats.show()
num4_stats = px.box(numerical_dataset[numerical_dataset['Num3'] <= 1], x="Residency", y="Num3", notched=True, points='all')
num4_stats.add_shape(type='line', x0='AU',y0=0.5,x1='US',y1=0.5,
                line=dict(color='Red',), xref='x', yref='y')
# num4_stats.show()








if savefigs:
    activity_table.write_image("outputs/plots/table.pdf")
    Support_AllCountries.write_image("outputs/plots/Support_AllCountries.pdf")
    freqset_1.write_image("outputs/plots/freqset_1.pdf")
    freqset_2.write_image("outputs/plots/freqset_2.pdf")
    freqset_3.write_image("outputs/plots/freqset_3.pdf")
    bayes_vaccine_global.write_image("outputs/plots/bayes_vaccine_global.pdf")
    naive_bayesian_vaccine_age_global.write_image("outputs/plots/naive_bayesian_vaccine_age_global.pdf")
    naive_bayesian_canadaq1_age_global.write_image("outputs/plots/naive_bayesian_canadaq1_age_global.pdf")
    num1_stats.write_image("outputs/plots/num1_stats.pdf")
    num2_stats.write_image("outputs/plots/num2a_stats.pdf")
    num3_stats.write_image("outputs/plots/num2b_stats.pdf")
    num4_stats.write_image("outputs/plots/num3_stats.pdf")



