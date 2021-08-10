import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
from scripts.frequents import apriori
from dash.dependencies import Input, Output, State
from scripts.dash_plots import *


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
            html.Div([
                html.H3('Column 1', style={'color': colors['text']}),
                html.P('Plot 5 description', style={'color': colors['text']}),
            ], className="six columns", style={'display': 'inline-block', 'width': '50vh', 'height': '30vh'}),
            html.Div([
                html.H3('Column 2', style={'color': colors['text']}),
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
                html.H3('Column 1', style={'color': colors['text']}),
                html.P('Plot 6 description', style={'color': colors['text']}),
            ], className="six columns", style={'display': 'inline-block', 'width': '50vh', 'height': '30vh'}),
            html.Div([
                html.H3('Column 2', style={'color': colors['text']}),
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
                html.H3('Column 1', style={'color': colors['text']}),
                html.P('Plot 7 description', style={'color': colors['text']}),
            ], className="six columns", style={'display': 'inline-block', 'width': '50vh', 'height': '30vh'}),
            html.Div([
                html.H3('Column 2', style={'color': colors['text']}),
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

        ## numerical plots
        html.Div([
            html.Div([
                html.H3('Column 1', style={'color': colors['text']}),
                html.P('Plot 8 description', style={'color': colors['text']}),
            ], className="six columns", style={'display': 'inline-block', 'width': '50vh', 'height': '30vh'}),
            html.Div([
                html.H3('Column 2', style={'color': colors['text']}),
                html.P("Graph 8 Hovermode", style={'color': colors['text']}),
                dcc.RadioItems(
                    id='hovermode_g8', style={'color': colors['text']},
                    labelStyle={'display': 'inline-block'},
                    options=[{'label': x, 'value': x} 
                            for x in ['x', 'x unified', 'closest']],
                    value='x unified'),
                dcc.Graph(
                    id='num1_stats',
                    figure=num1_stats,
                    ),
                    ], className="six columns"),
                ], className="row"),
        html.Div([
            html.Div([
                html.H3('Column 1', style={'color': colors['text']}),
                html.P('Plot 9 description', style={'color': colors['text']}),
            ], className="six columns", style={'display': 'inline-block', 'width': '50vh', 'height': '30vh'}),
            html.Div([
                html.H3('Column 2', style={'color': colors['text']}),
                html.P("Graph 9 Hovermode", style={'color': colors['text']}),
                dcc.RadioItems(
                    id='hovermode_g9', style={'color': colors['text']},
                    labelStyle={'display': 'inline-block'},
                    options=[{'label': x, 'value': x} 
                            for x in ['x', 'x unified', 'closest']],
                    value='x unified'),
                dcc.Graph(
                    id='num2_stats',
                    figure=num2_stats,
                    ),
                    ], className="six columns"),
                ], className="row"),
        html.Div([
            html.Div([
                html.H3('Column 1', style={'color': colors['text']}),
                html.P('Plot 10 description', style={'color': colors['text']}),
            ], className="six columns", style={'display': 'inline-block', 'width': '50vh', 'height': '30vh'}),
            html.Div([
                html.H3('Column 2', style={'color': colors['text']}),
                html.P("Graph 10 Hovermode", style={'color': colors['text']}),
                dcc.RadioItems(
                    id='hovermode_g10', style={'color': colors['text']},
                    labelStyle={'display': 'inline-block'},
                    options=[{'label': x, 'value': x} 
                            for x in ['x', 'x unified', 'closest']],
                    value='x unified'),
                dcc.Graph(
                    id='num3_stats',
                    figure=num3_stats,
                    ),
                    ], className="six columns"),
                ], className="row"),
        html.Div([
            html.Div([
                html.H3('Column 1', style={'color': colors['text']}),
                html.P('Plot 11 description', style={'color': colors['text']}),
            ], className="six columns", style={'display': 'inline-block', 'width': '50vh', 'height': '30vh'}),
            html.Div([
                html.H3('Column 2', style={'color': colors['text']}),
                html.P("Graph 11 Hovermode", style={'color': colors['text']}),
                dcc.RadioItems(
                    id='hovermode_g11', style={'color': colors['text']},
                    labelStyle={'display': 'inline-block'},
                    options=[{'label': x, 'value': x} 
                            for x in ['x', 'x unified', 'closest']],
                    value='x unified'),
                dcc.Graph(
                    id='num4_stats',
                    figure=num4_stats,
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
    Output("num1_stats", "figure"), 
    [Input("hovermode_g8", "value")], 
    [State('num1_stats', 'figure')])
def update_hovermode(mode, fig_json):
    fig = go.Figure(fig_json)
    fig.update_layout(hovermode=mode)
    return fig

@app.callback(
    Output("num2_stats", "figure"), 
    [Input("hovermode_g9", "value")], 
    [State('num2_stats', 'figure')])
def update_hovermode(mode, fig_json):
    fig = go.Figure(fig_json)
    fig.update_layout(hovermode=mode)
    return fig

@app.callback(
    Output("num3_stats", "figure"), 
    [Input("hovermode_g10", "value")], 
    [State('num3_stats', 'figure')])
def update_hovermode(mode, fig_json):
    fig = go.Figure(fig_json)
    fig.update_layout(hovermode=mode)
    return fig

@app.callback(
    Output("num4_stats", "figure"), 
    [Input("hovermode_g11", "value")], 
    [State('num4_stats', 'figure')])
def update_hovermode(mode, fig_json):
    fig = go.Figure(fig_json)
    fig.update_layout(hovermode=mode)
    return fig




if __name__ == '__main__':
    app.run_server()
