import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
from navbar import Navbar
from app import app

nav = Navbar()

df_stocks = pd.read_csv('Datasets/stocks.csv')
dates = df_stocks['Date']
dow = df_stocks['Dow_Jones_Index']
sp500 = df_stocks['S&P_500_Index']
nasdaq = df_stocks['Nasdaq']

trace1 = go.Scatter(x=dates, y=dow, mode='lines', name='DOW Jones', marker={'color': '#CD7F32'})
# trace2 = go.Scatter(x=dates, y=sp500, mode='lines', name='S&P 500 Index', marker={'color': '#CD7F32'})
# trace3 = go.Scatter(x=dates, y=nasdaq, mode='lines', name='Nasdaq Composite', marker={'color': '#CD7F32'})
data = [trace1]


layout = html.Div(children=[
    html.Div([
        html.H1(children='Stock Market',
                style={
                    'textAlign': 'center',
                    'color': 'white'
                }
                ),
        html.H3('Line chart', style={'color': 'white'}),
        html.Div('This chart represents the trend in the Dow Jones Industrial Average'),
        dcc.Graph(id='stocks-graph',
                  figure={'data': data,
                          'layout': go.Layout(title='Dow Jones Industrial Average',
                                              xaxis={'title': 'Date'}, yaxis={'title': 'Closing Index'})
                          },
                  ),
        html.Br(),
        html.P("The United States Stock Market has taken a major hit")
    ], className='graph-layout'),
])


def get_layout():
    complete_layout = html.Div([
        nav,
        layout
    ])
    return complete_layout
