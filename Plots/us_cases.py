import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go
from Plots import helper
from navbar import Navbar

nav = Navbar()

country = helper.Country()

trace1 = go.Bar(x=country.get_top_ten_confirmed_states(), y=country.get_top_ten_state_cases(),
                name='Cases', marker={'color': '#CD7F32'})
data_confirmed = [trace1]

# Layout
layout = html.Div(className='graph-layout', children=[
    html.H1(children='Cases from COVID-19 in the United States',
            style={
                'textAlign': 'center',
                'color': 'white'
            }
            ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bar chart', style={'color': 'white'}),
    html.Div('This chart represents the top ten states with confirmed cases.'),
    dcc.Graph(id='graph1',
              figure={'data': data_confirmed,
                      'layout': go.Layout(title='Top 10 Corona Virus Confirmed Cases by State',
                                          xaxis={'title': 'States'}, yaxis={'title': 'Number of confirmed cases'})
                      }
              ),
    html.Br(),
    html.Br(),
])


def get_layout():
    complete_layout = html.Div([
        nav,
        layout
    ])
    return complete_layout
