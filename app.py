import time
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import pandas_datareader.data as web
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px
from copy import copy
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import utils
import seaborn as sb



figcor = px.imshow(utils.returnarscorr)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], prevent_initial_callbacks=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )


app.layout = dbc.Container([
    dbc.Row([
         dbc.Col(html.H1("Dash ARS ADRs",
                        className='text-center text-primary, mb4'),
                width=12)  
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Div(children='''
        Normalized Merval price evolution. Select tickers: 
    ''', className='text-left bg-info'),
            dcc.Dropdown(id='my-dpdn', multi=True, value='GGAL.BA', options=[{'label':x, 'value': x}
                                                                             for x in utils.pricearsnorm.columns.tolist()]),
            dcc.Graph(id='line-fig', figure={})
        ], width={'size':6, 'order':1}),
        
        dbc.Col([
             html.Div(children='''
        Normalized ADR price evolution. Select tickers:
    ''', className='text-left bg-info'),
            dcc.Dropdown(id='my-dpdn2',multi=True, value=['GGAL','YPFD'], options=[{'label':x,'value':x}
                                                                                  for x in utils.priceusnorm.columns.tolist()]),
            dcc.Graph(id='line-fig2', figure={})
        ], width={'size':6, 'order':2})
    ], justify='around'),
    
    dbc.Row([
        dbc.Col([
            html.Div(children='''
        Daily ADR return distribution. Select tickers
    ''', className='text-left bg-info'),
            dcc.Dropdown(id='my-dpdn3', multi=True, value=['GGAL','YPFD'],
                         options=[{'label':x, 'value': x}
                                  for x in utils.priceus.columns.tolist()]),
            dcc.Graph(id='line-fig3', figure={})
        ], width={'size':6}),

        dbc.Col([
            html.Div(children='''
        Correlation map between Merval tickers
    ''', className='text-left bg-info'),
            dcc.Graph(id='line-fig4', figure = figcor)
        ], width={'size':6})    
        
    ], justify='around')
    
], fluid=True)


@app.callback(
    Output(component_id='line-fig', component_property='figure'),
    Input(component_id='my-dpdn', component_property='value')
)
def updategraph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))
    
    pricearsnormdash = utils.pricearsnorm.copy()
    pricearsnormdash = pricearsnormdash[option_slctd]
    pricearsnormdash['Date'] = utils.pricearsnorm['Date']
    
    fig = go.Figure()
    
    for ticker in option_slctd:
        fig.add_trace(go.Scatter(x=pricearsnormdash['Date'], y=pricearsnormdash[ticker],
                                mode= 'lines', name = ticker ))
    
    return fig

@app.callback(
    Output(component_id='line-fig2', component_property='figure'),
    [Input(component_id='my-dpdn2', component_property='value')]
)

def update_graph_scatter(option_slctd):
    print(option_slctd)
    print(type(option_slctd))
    
    priceusnormdash = utils.priceusnorm.copy()
    priceusnormdash = priceusnormdash[option_slctd]
    priceusnormdash['Date'] = utils.priceusnorm['Date']
    
    fig = go.Figure()
    
    for ticker in option_slctd:
        fig.add_trace(go.Scatter(x=priceusnormdash['Date'], y=priceusnormdash[ticker],
                                mode= 'lines', name = ticker ))
    
    return fig

@app.callback(
    Output(component_id='line-fig3', component_property='figure'),
    [Input(component_id='my-dpdn3', component_property='value')]
)

def update_graph_scatter(option_slctd):
    print(option_slctd)
    print(type(option_slctd))
    
    dfreturnus = utils.returnus.copy()
    dfreturnus = dfreturnus[option_slctd]
        
    
    fig = go.Figure()
    
    for ticker in option_slctd:
        fig.add_trace(go.Histogram(x=dfreturnus[ticker], name = ticker))
        fig.update_layout(barmode='stack')
        
    return fig



if __name__ == "__main__":
    app.run_server(debug=True)

