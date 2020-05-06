import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from Plots import helper
from navbar import Navbar

nav = Navbar()

country = helper.Country()

trace2 = go.Bar(x=country.get_top_ten_deaths_states(), y=country.get_top_ten_state_deaths(),
                name='Cases', marker={'color': '#CD7F32'})
data_bar = [trace2]
data_pie = [go.Pie(labels=country.get_top_ten_confirmed_states(),
                                  values=country.get_top_ten_state_deaths())]
# Layout
layout = html.Div(className='graph-layout', children=[
    html.A(id='us-deaths'),
    html.H1(children='Deaths from COVID-19 in the United States',
            style={
                'textAlign': 'center',
                'color': 'white'
            }
            ),
    html.H3('Bar chart', style={'color': 'white'}),
    html.Div('This bar chart represents the top ten states with the highest death count.'),
    dcc.Graph(id='graph2',
              figure={
                  'data': data_bar,
                  'layout': go.Layout(title='Corona Virus Deaths by State',
                                      xaxis={'title': 'States'}, yaxis={'title': 'Number of Deaths'})
              }
              ),
    html.Br(),
    html.Br(),
    html.H3('Pie Chart', style={'color': 'white'}),
    html.Div('This chart represents the top ten states with the highest death count.'),
    dcc.Graph(id='graph1',
              figure={
                  'data': data_pie,
              }
              )
])


def get_layout():
    complete_layout = html.Div([
        nav,
        layout
    ])
    return complete_layout
