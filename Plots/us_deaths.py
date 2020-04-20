import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go
from Plots import helper
from navbar import Navbar

nav = Navbar()

country = helper.Country()

trace2 = go.Bar(x=country.get_top_ten_deaths_states(), y=country.get_top_ten_state_deaths(),
                name='Cases', marker={'color': '#CD7F32'})
data_deaths = [trace2]

# Layout
layout = html.Div(className='graph-layout', children=[
    html.H1(children='Deaths from COVID-19 in the United States',
            style={
                'textAlign': 'center',
                'color': 'white'
            }
            ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bar chart', style={'color': 'white'}),
    html.Div('This bar chart represents the top ten states with the highest death count.'),
    dcc.Graph(id='graph2',
              figure={
                  'data': data_deaths,
                  'layout': go.Layout(title='Corona Virus Deaths by State',
                                      xaxis={'title': 'States'}, yaxis={'title': 'Number of Deaths'})
              }
              )
])


def get_layout():
    complete_layout = html.Div([
        nav,
        layout
    ])
    return complete_layout
