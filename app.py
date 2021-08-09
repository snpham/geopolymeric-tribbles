import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
from scripts.frequents import apriori
from dash.dependencies import Input, Output, State


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
activity_table.update_layout(plot_bgcolor=colors['background'],
                             paper_bgcolor=colors['background'])
# activity_table.write_image("outputs/plots/table.pdf")


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
for ii, country in enumerate(countries):
    df_country = dataset_country[dataset_country['Residency'] == country]
    minsup_country = min_sup * len(df_country)
    df_country = df_country.drop('Residency', axis=1)
    scans1_country, _, _ = apriori(df_country, minsup_country)
    scans1_country = {key:value/len(df_country) for (key, value) in scans1_country.items()}
    gobars.append(go.Bar(name=country, x=list(scans1_country.keys()), 
                         y=list(scans1_country.values()), base=0))
Support_AllCountries = go.Figure(data=gobars[:])
Support_AllCountries.update_layout(title=f'Support of Preparation Activities, by Country <br>'
                                         f'          - frequentset-1. min support: {min_sup}')
# Change the bar mode
Support_AllCountries.update_layout(barmode='relative', 
    xaxis=dict(title='activity',titlefont_size=16,tickfont_size=14),
    yaxis=dict(title='support',titlefont_size=16,tickfont_size=14),
    plot_bgcolor=colors['background'], paper_bgcolor=colors['background'],
    font_color=colors['text'], hovermode="x unified")


## graph 2 ##
update_layout = dict(barmode='group',
                    yaxis=dict( titlefont_size=16, tickfont_size=16, range=[0, 1]),
                    xaxis=dict( tickangle=-45, titlefont_size=16, tickfont_size=16),
                    plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],
                    font_color=colors['text'], hovermode="x unified",
                    hoverlabel=dict(font_size=14))
update_traces = dict(marker_color='#a0a4c0', marker_line_color='#52567A',
                    marker_line_width=1.5, opacity=0.7)

# get global frequentset-1
min_sup = 0.01
min_sup *= len(dataset_prep)
scan1, scan2, scan3 = apriori(dataset_prep, min_sup)
prep_merged = {key:value/len(dataset_prep) for (key, value) in scan1.items()}
prep_merged = pd.DataFrame.from_dict(prep_merged, orient='index', 
                                     columns=['support'])
freqset_1 = px.bar(prep_merged, y='support', x=prep_merged.index, 
                   labels={'index': 'activity'})
freqset_1.update_layout(title=f'Support of Preparation Activities by Country <br>'
                f'          - frequentset-1. min support: {min_sup/len(dataset_prep)}')
freqset_1.update_traces(update_traces)
freqset_1.update_layout(update_layout)


## graph 3 ##
# increase support and view higher frequentsets (2 and 3)
min_sup = 0.5
min_sup *= len(dataset_prep)
scan1, scan2, scan3 = apriori(dataset_prep, min_sup)
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


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
        meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}])
server = app.server
app.title='COVID-19 Misinformation Project'


########### Set up the layout
app.layout = html.Div(style={'backgroundColor': colors['background']}, 
    children=[
        html.H1('CSCI-5502 Project', style={'color': colors['text']}),
        html.Div([
            html.Div([
                html.H3('Column 1', style={'color': colors['text']}),
                html.P('Table description', style={'color': colors['text']}),
            ], className="six columns", style={'display': 'inline-block', 'width': '50vh', 'height': '30vh'}),
            html.Div([
                dcc.Graph(
                id='activity_table',
                figure=activity_table,
                ),
                    ], className="six columns"),
                ], className="row"),
        html.Div([
            html.Div([
                html.H3('Column 1', style={'color': colors['text']}),
                html.P('Plot 1 description', style={'color': colors['text']}),
            ], className="six columns", style={'display': 'inline-block', 'width': '50vh', 'height': '30vh'}),
            html.Div([
                html.H3('Column 2', style={'color': colors['text']}),
                html.P("Graph 1 Hovermode", style={'color': colors['text']}),
                dcc.RadioItems(
                    id='hovermode_g1', style={'color': colors['text']},
                    labelStyle={'display': 'inline-block'},
                    options=[{'label': x, 'value': x} 
                            for x in ['x', 'x unified', 'closest']],
                    value='x unified'),
                dcc.Graph(
                    id='Support_AllCountries',
                    figure=Support_AllCountries,
                    ),
                    ], className="six columns"),
                ], className="row"),
        html.Div([
            html.Div([
                html.H3('Column 1', style={'color': colors['text']}),
                html.P('Plot 2 description', style={'color': colors['text']}),
            ], className="six columns", style={'display': 'inline-block', 'width': '50vh', 'height': '30vh'}),
            html.Div([
                html.H3('Column 2', style={'color': colors['text']}),
                html.P("Graph 2 Hovermode", style={'color': colors['text']}),
                dcc.RadioItems(
                    id='hovermode_g2', style={'color': colors['text']},
                    labelStyle={'display': 'inline-block'},
                    options=[{'label': x, 'value': x} 
                            for x in ['x', 'x unified', 'closest']],
                    value='x unified'),
                dcc.Graph(
                    id='freqset_1',
                    figure=freqset_1,
                    ),
                    ], className="six columns"),
                ], className="row"),
        html.Div([
            html.Div([
                html.H3('Column 1', style={'color': colors['text']}),
                html.P('Plot 3 description', style={'color': colors['text']}),
            ], className="six columns", style={'display': 'inline-block', 'width': '50vh', 'height': '30vh'}),
            html.Div([
                html.H3('Column 2', style={'color': colors['text']}),
                html.P("Graph 3 Hovermode", style={'color': colors['text']}),
                dcc.RadioItems(
                    id='hovermode_g3', style={'color': colors['text']},
                    labelStyle={'display': 'inline-block'},
                    options=[{'label': x, 'value': x} 
                            for x in ['x', 'x unified', 'closest']],
                    value='x unified'),
                dcc.Graph(
                    id='freqset_2',
                    figure=freqset_2,
                    ),
                    ], className="six columns"),
                ], className="row"),
        html.Div([
            html.Div([
                html.H3('Column 1', style={'color': colors['text']}),
                html.P('Plot 4 description', style={'color': colors['text']}),
            ], className="six columns", style={'display': 'inline-block', 'width': '50vh', 'height': '30vh'}),
            html.Div([
                html.H3('Column 2', style={'color': colors['text']}),
                html.P("Graph 4 Hovermode", style={'color': colors['text']}),
                dcc.RadioItems(
                    id='hovermode_g4', style={'color': colors['text']},
                    labelStyle={'display': 'inline-block'},
                    options=[{'label': x, 'value': x} 
                            for x in ['x', 'x unified', 'closest']],
                    value='x unified'),
                dcc.Graph(
                    id='freqset_3',
                    figure=freqset_3,
                    ),
                    ], className="six columns"),
                ], className="row"),
        html.Div([
            html.A('Project Code on Github', 
                href='https://github.com/summeryriddles/geopolymeric-tribbles'),
            html.Br(),])
        ]
    )


@app.callback(
    Output("Support_AllCountries", "figure"), 
    [Input("hovermode_g1", "value")], 
    [State('Support_AllCountries', 'figure')])
def update_hovermode(mode, fig_json):
    fig = go.Figure(fig_json)
    fig.update_layout(hovermode=mode)
    return fig

@app.callback(
    Output("freqset_1", "figure"), 
    [Input("hovermode_g2", "value")], 
    [State('freqset_1', 'figure')])
def update_hovermode(mode, fig_json):
    fig = go.Figure(fig_json)
    fig.update_layout(hovermode=mode)
    return fig

@app.callback(
    Output("freqset_2", "figure"), 
    [Input("hovermode_g3", "value")], 
    [State('freqset_2', 'figure')])
def update_hovermode(mode, fig_json):
    fig = go.Figure(fig_json)
    fig.update_layout(hovermode=mode)
    return fig

@app.callback(
    Output("freqset_3", "figure"), 
    [Input("hovermode_g4", "value")], 
    [State('freqset_3', 'figure')])
def update_hovermode(mode, fig_json):
    fig = go.Figure(fig_json)
    fig.update_layout(hovermode=mode)
    return fig



if __name__ == '__main__':
    app.run_server()
