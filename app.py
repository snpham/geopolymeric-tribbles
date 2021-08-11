import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from scripts.dash_plots import *
from scripts.Kmeans_plots import *
from scripts.RyanSumCharts import *


Trustingroups = ['Trustingroups_1', 'Trustingroups_2', 'Trustingroups_3', 'Trustingroups_4', 'Trustingroups_5',
                 'Trustingroups_6', 'Trustingroups_7', 'Trustingroups_8', 'Trustingroups_9', 'Trustingroups_10',
                 'Trustingroups_11', 'Trustingroups_12', 'Trustingroups_13']
numerical_dataset = pd.read_csv('outputs/numerical_dataset.csv')

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
        html.Div([html.Br(),html.Br(),html.Br(),html.Br()]),

        # ## ryan's exploratory stats
        html.Div([
            html.Div([
                html.H3('Exploratory Statistics', style={'color': colors['text']}),
                html.P(' ', style={'color': colors['text']}),
            ], className="five columns", style={'display': 'inline-block', 'width': '40hh', 'height': '30vh'}),
            html.Div([
                html.H3('Exploratory Statistics - Political Leaning', style={'color': colors['text']}),
                dcc.Graph(
                    id='plot1',
                    figure=plot1,
                    ),
                    ], className="six columns"),
                ], className="row"),
        html.Div([
            html.Div([
                html.H3('Exploratory Statistics', style={'color': colors['text']}),
                html.P(' ', style={'color': colors['text']}),
            ], className="five columns", style={'display': 'inline-block', 'width': '40hh', 'height': '30vh'}),
            html.Div([
                html.H3('Exploratory Statistics - Political Leaning Breakdown', style={'color': colors['text']}),
                dcc.Graph(
                    id='plot2',
                    figure=plot2,
                    ),
                    ], className="six columns"),
                ], className="row"),
        html.Div([
            html.Div([
                html.H3('Exploratory Statistics', style={'color': colors['text']}),
                html.P(' ', style={'color': colors['text']}),
            ], className="five columns", style={'display': 'inline-block', 'width': '40hh', 'height': '30vh'}),
            html.Div([
                html.H3('Exploratory Statistics - Severity of COVID', style={'color': colors['text']}),
                dcc.Graph(
                    id='plot3',
                    figure=plot3,
                    ),
                    ], className="six columns"),
                ], className="row"),
        html.Div([
            html.Div([
                html.H3('Exploratory Statistics', style={'color': colors['text']}),
                html.P(' ', style={'color': colors['text']}),
            ], className="five columns", style={'display': 'inline-block', 'width': '40hh', 'height': '30vh'}),
            html.Div([
                html.H3('Exploratory Statistics - Worry about COVID', style={'color': colors['text']}),
                dcc.Graph(
                    id='plot4',
                    figure=plot4,
                    ),
                    ], className="six columns"),
                ], className="row"),

        ## numerical plots
        html.Div([
            html.Div([
                html.H3('Exploratory Statistics - Numerical', style={'color': colors['text']}),
                html.P(['Num1: Out of 1,000 people in a small town 500 are members of a choir.'
                       ' Out of these 500 members in the choir 100 are men.'
                       ' Out of the 500 inhabitants that are not in the choir 300 are men.'
                       ' What is the probability that a randomly drawn man is a member of the choir?'
                       ' Please indicate the probability in percent.        ____ %',
                       html.Br(),html.Br(),
                       'Num2a: Imagine we are throwing a five-sided die 50 times.'
                       'On average, out of these 50 throws how many times would this'
                       ' five-sided die show an odd number (1, 3 or 5)?  ____ out of 50 throws.', 
                       html.Br(), html.Br(),
                       'Num2b: Imagine we are throwing a loaded die (6 sides) 70 times.'
                       'The probability that the die shows a 6 is twice as high as the'
                       ' probability of each of the other numbers. On average, out of these 70'
                       ' throws how many times would the die show the number 6?'
                       ' ____ out of 70 throws.',
                       html.Br(),html.Br(),
                       'Num3: In a forest 20% of mushrooms are red, 50% brown and 30% white.'
                       ' A red mushroom is poisonous with a probability of 20%. A mushroom'
                       ' that is not red is poisonous with a probability of 5%.'
                       ' What is the probability that a poisonous mushroom in the forest is red?'
                       ' ____ %'
                ], style={'color': colors['text']}),
            ], className="five columns", style={'display': 'inline-block', 'width': '40hh', 'height': '30vh'}),
            html.Div([
                html.H3('Exploratory Statistics - Numerical', style={'color': colors['text']}),
                html.P('Select a Numerical Attribute to View Statistical Parameters', style={'color': colors['text']}),
                dcc.RadioItems(
                    id='numeric_radio', 
                    options=[{'value': x, 'label': x} 
                            for x in ['Num1', 'Num2a', 'Num2b', 'Num3']],
                    value='Num1', 
                    labelStyle={'display': 'inline-block'},
                    style={'color': colors['text']}
                ),
                dcc.Graph(id="numeric_stats"),
                    ], className="six columns"),
                ], className="row"),
        html.Div([html.Br(),html.Br(),html.Br(),html.Br(),html.Br()]),


        # apriori
        html.Div([
            html.Div([
                html.H3('Apriori Analysis', style={'color': colors['text']}),
                html.P('Preparation Activities Table', style={'color': colors['text']}),
                dcc.Graph(
                id='activity_table',
                figure=activity_table,
                ),
            ], className="five columns", style={'display': 'inline-block', 'width': '40hh', 'height': '30vh'}),
            html.Div([
                html.H3('Apriori Analysis - Preparation Support by Country', style={'color': colors['text']}),
                html.P("Select Graph 1 Hovermode", style={'color': colors['text']}),
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
        # frequent-1/2/3 apriori with slider
        html.Div([
            html.Div([
                html.H3('Apriori Analysis', style={'color': colors['text']}),
                html.P('Global Frequent-1/2/3 Itemsets', style={'color': colors['text']}),
            ], className="five columns", style={'display': 'inline-block', 'width': '40hh', 'height': '30vh'}),
            html.Div([
                html.H3('Apriori Analysis - Global Frequent-1/2/3 Graph', style={'color': colors['text']}),
                html.P('Select a Support Level', style={'color': colors['text']}),
                dcc.Slider(
                    id='apriori_sup2_slider',
                    tooltip = { 'always_visible': True },
                    min=0,
                    max=1,
                    step=0.01,
                    value=0.4,),
                html.P('Select a Frequent-set', style={'color': colors['text']}),
                dcc.RadioItems(
                    id='apriori_sup2_radio',
                    options=[{'label': i, 'value': i} for i in ['Frequent-1', 'Frequent-2', 'Frequent-3']],
                    value='Frequent-2',
                    labelStyle={'display': 'inline-block'},
                    style={'color': colors['text']}),
                dcc.Graph(
                    id='apriori_sup2',
                    ),
                    ], className="six columns"),
                ], className="row"),
        html.Div([html.Br(),html.Br(),html.Br(),html.Br(),html.Br()]),

        # bayesian
        html.Div([
            html.Div([
                html.H3('Decision Tree Analysis', style={'color': colors['text']}),
                html.P('Information Gain Table', style={'color': colors['text']}),
                html.P('Six highest and six lowest information gain', style={'color': colors['text']}),
                dcc.Graph(
                id='gain_table',
                figure=gain_table,
                ),
            ], className="five columns", style={'display': 'inline-block', 'width': '40hh', 'height': '30vh'}),
            html.Div([
                html.H3('Decision Tree - Probability of Vaccination and Recommendation', style={'color': colors['text']}),
                html.P("Graph 5 Hovermode", style={'color': colors['text']}),
                dcc.RadioItems(
                    id='hovermode_g5', style={'color': colors['text']},
                    labelStyle={'display': 'inline-block'},
                    options=[{'label': x, 'value': x} 
                            for x in ['x', 'x unified', 'closest']],
                    value='x unified'),
                dcc.Graph(
                    id='bayes_vaccine_global',
                    figure=bayes_vaccine_global,
                    ),
                    ], className="six columns"),
                ], className="row"),
        html.Div([
            html.Div([
                html.H3('Naive Bayesian Analysis - VaccineQ1, Q2', style={'color': colors['text']}),
                html.P(' ', style={'color': colors['text']}),
            ], className="five columns", style={'display': 'inline-block', 'width': '40hh', 'height': '30vh'}),
            html.Div([
                html.H3('Naive Bayesian Analysis', style={'color': colors['text']}),
                html.P("Graph 6 Hovermode", style={'color': colors['text']}),
                dcc.RadioItems(
                    id='hovermode_g6', style={'color': colors['text']},
                    labelStyle={'display': 'inline-block'},
                    options=[{'label': x, 'value': x} 
                            for x in ['x', 'x unified', 'closest']],
                    value='x unified'),
                dcc.Graph(
                    id='naive_bayesian_vaccine_age_global',
                    figure=naive_bayesian_vaccine_age_global,
                    ),
                    ], className="six columns"),
                ], className="row"),
        html.Div([
            html.Div([
                html.H3('Naive Bayesian Analysis', style={'color': colors['text']}),
                html.P(' ', style={'color': colors['text']}),
            ], className="five columns", style={'display': 'inline-block', 'width': '40hh', 'height': '30vh'}),
            html.Div([
                html.H3('Naive Bayesian Analysis - CanadaQ1', style={'color': colors['text']}),
                html.P("Graph 7 Hovermode", style={'color': colors['text']}),
                dcc.RadioItems(
                    id='hovermode_g7', style={'color': colors['text']},
                    labelStyle={'display': 'inline-block'},
                    options=[{'label': x, 'value': x} 
                            for x in ['x', 'x unified', 'closest']],
                    value='x unified'),
                dcc.Graph(
                    id='naive_bayesian_canadaq1_age_global',
                    figure=naive_bayesian_canadaq1_age_global,
                    ),
                    ], className="six columns"),
                ], className="row"),
        html.Div([html.Br(),html.Br(),html.Br(),html.Br(),html.Br()]),


        ## reiko's clustering
        html.Div([
            html.Div([
                html.H3('Clustering - DBSCAN', style={'color': colors['text']}),
                html.P(' ', style={'color': colors['text']}),
            ], className="five columns", style={'display': 'inline-block', 'width': '40hh', 'height': '30vh'}),
            html.Div([
                html.H3('DBSCAN Method - Social Media Trust', style={'color': colors['text']}),
                dcc.Graph(
                    id='SocialmediatrustQ1',
                    figure=SocialmediatrustQ1,
                    ),
                    ], className="six columns"),
                ], className="row"),
        html.Div([
            html.Div([
                html.H3('Clustering - DBSCAN', style={'color': colors['text']}),
                html.P(' ', style={'color': colors['text']}),
            ], className="five columns", style={'display': 'inline-block', 'width': '40hh', 'height': '30vh'}),
            html.Div([
                html.H3('DBSCAN Method - Politics', style={'color': colors['text']}),
                dcc.Graph(
                    id='Politics',
                    figure=Politics,
                    ),
                    ], className="six columns"),
                ], className="row"),
        html.Div([html.Br(),html.Br(),html.Br(),html.Br(),html.Br()]),


        # kyle's clusters
        html.Div([
            html.Div([
                html.H3('Clustering - K-Means', style={'color': colors['text']}),
                html.P(' ', style={'color': colors['text']}),
            ], className="five columns", style={'display': 'inline-block', 'width': '40hh', 'height': '30vh'}),
            html.Div([
                html.H3('Clustering - K-Means: Who vs Trust, All Groups', style={'color': colors['text']}),
                dcc.Graph(
                    id='WHOvTrustTot',
                    figure=WHOvTrustTot,
                    ),
                    ], className="six columns"),
                ], className="row"),
        html.Div([
            html.Div([
                html.H3('Clustering - K-Means', style={'color': colors['text']}),
                html.P(' ', style={'color': colors['text']}),
            ], className="five columns", style={'display': 'inline-block', 'width': '40hh', 'height': '30vh'}),
            html.Div([
                html.H3('Clustering - K-Means: Who vs Trust, Government', style={'color': colors['text']}),
                dcc.Graph(
                    id='WHOvTrustGov',
                    figure=WHOvTrustGov,
                    ),
                    ], className="six columns"),
                ], className="row"),
        html.Div([
            html.Div([
                html.H3('Clustering - K-Means', style={'color': colors['text']}),
                html.P(' ', style={'color': colors['text']}),
            ], className="five columns", style={'display': 'inline-block', 'width': '40hh', 'height': '30vh'}),
            html.Div([
                html.H3('Clustering - K-Means: COVID Estimates vs. Trust, All Groups', style={'color': colors['text']}),
                dcc.Graph(
                    id='EstimatesvTrustTot',
                    figure=EstimatesvTrustTot,
                    ),
                    ], className="six columns"),
                ], className="row"),
        html.Div([
            html.Div([
                html.H3('Clustering - K-Means', style={'color': colors['text']}),
                html.P(' ', style={'color': colors['text']}),
            ], className="five columns", style={'display': 'inline-block', 'width': '40hh', 'height': '30vh'}),
            html.Div([
                html.H3('Clustering - K-Means: COVID Worry vs. Affected', style={'color': colors['text']}),
                dcc.Graph(
                    id='WorryvAffected',
                    figure=WorryvAffected,
                    ),
                    ], className="six columns"),
                ], className="row"),
        html.Div([
            html.Div([
                html.H3('Clustering - K-Means', style={'color': colors['text']}),
                html.P(' ', style={'color': colors['text']}),
            ], className="five columns", style={'display': 'inline-block', 'width': '40hh', 'height': '30vh'}),
            html.Div([
                html.H3('Clustering - K-Means: Social Media Use vs. Affected', style={'color': colors['text']}),
                dcc.Graph(
                    id='SocialvAffected',
                    figure=SocialvAffected,
                    ),
                    ], className="six columns"),
                ], className="row"),



        ## templates for dropdowns
        # html.Div([
        #     html.Div([
        #         html.H3('Column 1', style={'color': colors['text']}),
        #         html.P('Plot 2 description', style={'color': colors['text']}),
        #     ], className="five columns", style={'display': 'inline-block', 'width': '40hh', 'height': '30vh'}),
        #     html.Div([
        #         html.H3('Column 2', style={'color': colors['text']}),
        #         dcc.Dropdown(
        #                     id = "attr_dropdown",
        #                     options=[{'label': i, 'value': i} for i in Trustingroups],
        #                     placeholder = "Select Attribute"),
        #         dcc.Graph(
        #             id='bayes_fig',
        #             figure=go.Figure(),
        #             ),
        #             ], className="six columns"),
        #         ], className="row"),


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

@app.callback(
    Output("bayes_vaccine_global", "figure"), 
    [Input("hovermode_g5", "value")], 
    [State('bayes_vaccine_global', 'figure')])
def update_hovermode(mode, fig_json):
    fig = go.Figure(fig_json)
    fig.update_layout(hovermode=mode)
    return fig

@app.callback(
    Output("naive_bayesian_vaccine_age_global", "figure"), 
    [Input("hovermode_g6", "value")], 
    [State('naive_bayesian_vaccine_age_global', 'figure')])
def update_hovermode(mode, fig_json):
    fig = go.Figure(fig_json)
    fig.update_layout(hovermode=mode)
    return fig

@app.callback(
    Output("naive_bayesian_canadaq1_age_global", "figure"), 
    [Input("hovermode_g7", "value")], 
    [State('naive_bayesian_canadaq1_age_global', 'figure')])
def update_hovermode(mode, fig_json):
    fig = go.Figure(fig_json)
    fig.update_layout(hovermode=mode)
    return fig

@app.callback(
    Output("SocialmediatrustQ1", "figure"), 
    [Input("hovermode_g12", "value")], 
    [State('SocialmediatrustQ1', 'figure')])
def update_hovermode(mode, fig_json):
    fig = go.Figure(fig_json)
    fig.update_layout(hovermode=mode)
    return fig

@app.callback(
    Output("Politics", "figure"), 
    [Input("hovermode_g13", "value")], 
    [State('Politics', 'figure')])
def update_hovermode(mode, fig_json):
    fig = go.Figure(fig_json)
    fig.update_layout(hovermode=mode)
    return fig




@app.callback(
    Output(component_id='bayes_fig',component_property='figure'),
    [Input(component_id='attr_dropdown', component_property='value')]
)
def update_map(attr_val):
    dataset = pd.read_csv('outputs/naive_bayesian_canada1_global.csv', index_col=0, header=0)
    naive_bayesian_canadaq1_age_global = go.Figure(data=
        [go.Bar(name='Serious-Yes Probability', x=dataset['age_range'].unique(), 
                            y=dataset['Serious-Yes Probability'], base=0),
        go.Bar(name='Serious-No Probability', x=dataset['age_range'].unique(), 
                            y=dataset['Serious-No Probability'], base=0),
                            ])
    naive_bayesian_canadaq1_age_global.update_layout(title=f"Naive Bayesian - {attr_val}, by Age Group")
    naive_bayesian_canadaq1_age_global.update_traces(dict(marker_line_width=1.5, opacity=0.7))
    # naive_bayesian_canadaq1_age_global.update_layout(update_layout_colorful)
    return naive_bayesian_canadaq1_age_global

@app.callback(
    Output('apriori_sup2', 'figure'),
    [Input('apriori_sup2_slider', 'value'),
     Input('apriori_sup2_radio', 'value')])
def update_output(value, freqs):
    min_sup = value
    min_sup *= len(dataset_prep)
    scan1, scan2, scan3 = apriori(dataset_prep, min_sup)
    if freqs == 'Frequent-1':
        df_scan1 = pd.DataFrame(data=scan1.items(), index=None, 
                                columns=['activity', 'value']).astype('int')
        df_scan1 = df_scan1.sort_values(by=['activity'], ascending=True)
        scan1 = dict(zip(df_scan1.iloc[:,0], df_scan1.iloc[:,1]))
        prep2 =  {key:value/len(dataset_prep) for (key, value) in scan1.items()}
    if freqs == 'Frequent-2':
        prep2 =  {key:value/len(dataset_prep) for (key, value) in scan2.items()}
    elif freqs == 'Frequent-3':
        prep2 =  {key:value/len(dataset_prep) for (key, value) in scan3.items()}
    prep2_supp = pd.DataFrame.from_dict(prep2, orient='index', 
                                        columns=['support'])
    freqset_plot = px.bar(prep2_supp, x=prep2_supp.index, y='support', 
                    labels={'index': 'activities'})
    freqset_plot.update_traces(update_traces)
    freqset_plot.update_layout(update_layout)
    freqset_plot.update_layout(hoverlabel=dict(
                                bgcolor="#cacdeb",
                                font_size=14,))
    freqset_plot.update_layout(dict(yaxis=dict(range=[0.0, 0.9])))
    freqset_plot.update_layout(title=f'Support of Preparation Activities, Global <br>'
                    f'         - {freqs}. min support: {min_sup/len(dataset_prep)}')
    return freqset_plot


















@app.callback(
    Output(component_id='numeric_stats',component_property='figure'),
    [Input(component_id='numeric_radio', component_property='value')]
)
def update_numeric(numeric_attr):
    if numeric_attr == 'Num1':
        num_plot = px.box(numerical_dataset, x="Residency", y="Num1", notched=True, points='all')
        num_plot.add_shape(type='line', x0='AU',y0=0.25,x1='US',y1=0.25,
                        line=dict(color='Red',), xref='x', yref='y')
    if numeric_attr == 'Num2a':
        num_plot = px.box(numerical_dataset, x="Residency", y="Num2a", notched=True, points='all')
        num_plot.add_shape(type='line', x0='AU',y0=0.6,x1='US',y1=0.6,
                        line=dict(color='Red',), xref='x', yref='y')
    if numeric_attr == 'Num2b':
        num_plot = px.box(numerical_dataset, x="Residency", y="Num2b", notched=True, points='all')
        num_plot.add_shape(type='line', x0='AU',y0=0.285714,x1='US',y1=0.285714,
                        line=dict(color='Red',), xref='x', yref='y')
    if numeric_attr == 'Num3':
        num_plot = px.box(numerical_dataset[numerical_dataset['Num3'] <= 1], x="Residency", y="Num3", notched=True, points='all')
        num_plot.add_shape(type='line', x0='AU',y0=0.5,x1='US',y1=0.5,
                        line=dict(color='Red',), xref='x', yref='y')
    update_layout_colorful = dict(barmode='relative', 
        xaxis=dict(title='country',titlefont_size=16,tickfont_size=14),
        yaxis=dict(title='normalized results',titlefont_size=16,tickfont_size=14),
         paper_bgcolor='#262738',
        font_color=colors['text'], hovermode="x unified")
    num_plot.update_layout(update_layout_colorful)
    return num_plot





if __name__ == '__main__':
    app.run_server()
