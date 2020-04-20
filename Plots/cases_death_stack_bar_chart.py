import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
from Plots import helper
from navbar import Navbar
from app import app

nav = Navbar()

# Most recent date on the csv's in Datasets
date_for_graph = '4/14/20'

# Load CSV files from Datasets folder
df_confirmed = pd.read_csv('Datasets/time_series_covid19_confirmed_US.csv')
df_deaths = pd.read_csv('Datasets/time_series_covid19_deaths_US.csv')


states = helper.States()
states.set_state("North Carolina")

# Layout
layout = html.Div(children=[
    html.H1(children='COVID-19 Dash',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div('Web dashboard for Coronavirus Data', style={'textAlign': 'center'}),
    html.Div('Coronavirus COVID-19 County Cases and Deaths', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Interactive Stack Bar chart', style={'color': '#df1e56'}),
    html.Div(
        'This chart represents the total of confirmed cases and deaths in the first 20 counties of selected state.'),
    dcc.Graph(id='cases-death-stack-bar-chart-state-graph'),
    html.Div('Please select a state', style={'color': '#ef3e18', 'margin': '10px'}),
    dcc.Dropdown(
        id='cases-death-stack-bar-chart-state-dropdown',
        options=[
            {'label': k, 'value': k} for k in states.get_state_index_code_keys()
        ],
        value='North Carolina'
    )
])


@app.callback(Output('cases-death-stack-bar-chart-state-graph', 'figure'),
              [Input('cases-death-stack-bar-chart-state-dropdown', 'value')])
def update_figure(selected_state):
    states.set_state(selected_state)

    date = date_for_graph

    filtered_df_confirmed = df_confirmed[df_confirmed['Province_State'] == selected_state]
    filtered_df_deaths = df_deaths[df_deaths['Province_State'] == selected_state]

    new_df_confirmed = filtered_df_confirmed.groupby(['Admin2'])[date].sum().reset_index()
    new_df_deaths = filtered_df_deaths.groupby(['Admin2'])[date].sum().reset_index()

    # Sorting values and select first 20 Counties
    if selected_state == 'Hawaii' or selected_state == 'Delaware' or selected_state == 'Connecticut':
        new_df_confirmed = new_df_confirmed.sort_values(by=[date], ascending=[False]).head(4).reset_index()
        new_df_deaths = new_df_deaths.sort_values(by=[date], ascending=[False]).head(4).reset_index()
    else:
        new_df_confirmed = new_df_confirmed.sort_values(by=[date], ascending=[False]).head(10).reset_index()
        new_df_deaths = new_df_deaths.sort_values(by=[date], ascending=[False]).head(10).reset_index()

    # Preparing data
    trace1 = go.Bar(x=new_df_confirmed['Admin2'], y=new_df_confirmed[date], name='Confirmed',
                    marker={'color': '#CD7F32'})
    trace2 = go.Bar(x=new_df_deaths['Admin2'], y=new_df_deaths[date], name='Deaths',
                    marker={'color': '#9EA0A1'})

    data = [trace1, trace2]
    return {'data': data,
            'layout': go.Layout(
                title='Total number of Confirmed Cases and Deaths by County as of {0}'.format(date),
                xaxis={'title': 'County'},
                yaxis={'title': 'Number of confirmed cases and deaths'},
                barmode='stack')}


def get_layout():
    complete_layout = html.Div([
        nav,
        layout
    ])
    return complete_layout
