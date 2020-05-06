import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from Plots import helper
from navbar import Navbar
import pandas as pd

nav = Navbar()

country = helper.Country()

trace1 = go.Bar(x=country.get_top_ten_confirmed_states(), y=country.get_top_ten_state_cases(),
                name='Cases', marker={'color': '#CD7F32'})
data_bar = [trace1]

data_pie = [go.Pie(labels=country.get_top_ten_confirmed_states(),
                                  values=country.get_top_ten_state_cases())]

# Population trends
df_population = pd.read_csv('Datasets/co-est2019-alldata.csv', encoding='ISO-8859–1')
df_usa = pd.read_csv('Datasets/USA-05-04-2020.csv')
df_usa = df_usa[df_usa['Country_Region'] == 'US']

# Column of unique state names and confirmed cases
df_states = df_usa.groupby(['Province_State'])['Confirmed'].sum().reset_index()
# Removing values not available in population dataset
df_states = df_states.drop([8, 12, 13, 38, 43, 44, 52])
# Removed rows, resetting index to correspond with other dataframe
df_states = df_states.reset_index(drop=True)
# Order by number of cases
df_states = df_states.sort_values(by=['Confirmed'], ascending=[False]).reset_index()

# Column of state names and their population estimates
df = df_population.groupby(['STNAME'])['POPESTIMATE2019'].sum().reset_index()

# Reindex df by order of df_states
indexes_by_cases = df_states['index'].to_list()
df = df.reindex(indexes_by_cases)
# Only take the top 10 states in confirmed cases
df = df.head(10)
df = df.reset_index()
cases_per_population = country.get_top_ten_state_cases()/(df['POPESTIMATE2019']/2)
pop_trace = go.Bar(x=country.get_top_ten_confirmed_states(), y=cases_per_population,
                   name='Case by Population', marker={'color': '#CD7F32'})
pop_data = [pop_trace]

# Layout
layout = html.Div(className='graph-layout', children=[
    html.A(id='us-cases'),
    html.H1(children='Cases of COVID-19 in the United States',
            style={
                'textAlign': 'center',
                'color': 'white'
            }
            ),
    html.H3('Bar chart', style={'color': 'white'}),
    html.Div('This chart represents the top ten states with confirmed cases.'),
    dcc.Graph(id='graph1',
              figure={'data': data_bar,
                      'layout': go.Layout(title='Top 10 Corona Virus Confirmed Cases by State',
                                          xaxis={'title': 'States'}, yaxis={'title': 'Number of confirmed cases'})
                      }
              ),
    html.Br(),
    html.Br(),
    html.H3('Pie Chart', style={'color': 'white'}),
    html.Div('This chart represents the top ten states with confirmed cases.'),
    dcc.Graph(id='graph1',
              figure={
                  'data': data_pie,
              }
              ),
    html.Br(),
    html.Br(),
    html.H1(children='Cases from COVID-19 Relative to Population',
            style={
                'textAlign': 'center',
                'color': 'white'
            }),
    html.H3('Bar Chart', style={'color': 'white'}),
    html.Div('This chart represents the number of cases relative to total state population as a percent.'),
    dcc.Graph(id='graph1',
              figure={'data': pop_data,
                      'layout': go.Layout(xaxis={'title': 'States'}, yaxis=dict({'title': 'Cases Out of Population'}, tickformat=".2%"))
                      }
              ),
                  ])


def get_layout():
    complete_layout = html.Div([
        nav,
        layout
    ])
    return complete_layout
