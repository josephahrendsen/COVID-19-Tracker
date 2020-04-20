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

states = helper.States()
states.set_state("North Carolina")

# Layout
layout = html.Div(className='graph-layout', children=[
    html.H1(children='Daily Cases of COVID-19 in Each State and County',
            style={
                'textAlign': 'center',
                'color': 'white'
            }
            ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Interactive Line chart', style={'color': 'white'}),
    html.Div('This chart represents the amount of daily confirmed cases reported each day'),
    html.Div('Please select a state', style={'color': '#ef3e18'}),
    dcc.Dropdown(
        id='daily-state-dropdown-bar-graph',
        options=[
            {'label': k, 'value': k} for k in states.get_state_index_code_keys()
        ],
        value='North Carolina',
        style={'color': 'black'}
    ),
    dcc.Graph(id='daily-state-bar-graph'),
    html.Br(),
    html.Div('This chart represents the total number of daily confirmed cases in a county'),
    html.Div('Please select a county', style={'color': '#ef3e18'}),
    dcc.Dropdown(
        id='daily-county-dropdown-bar-graph',
        options=[],
        value=states.get_counties_in_state()[0],
        style={'color': 'black'}
    ),
    dcc.Graph(id='daily-county-bar-graph'),
    html.Br(),
    html.Br()
])


@app.callback(Output('daily-state-bar-graph', 'figure'),
              [Input('daily-state-dropdown-bar-graph', 'value')])
def update_graph1(selected_state):
    """Return a graph

    Update state graph with selected state
    """
    states.set_state(selected_state)

    # Preparing Data
    cases = helper.Confirmed(selected_state)

    trace1 = go.Bar(x=cases.get_dates_since_start(), y=cases.get_daily_state_cases(),
                        name='Cases')
    data = [trace1]
    state_graph = {'data': data,
                   'layout': go.Layout(
                       title='New Daily Confirmed Cases in ' + cases.get_state_name(),
                       xaxis={'title': 'Date'},
                       yaxis={'title': 'Number of confirmed cases'})}
    return state_graph


@app.callback(
    Output('daily-county-bar-graph', 'figure'),
    [Input('daily-state-dropdown-bar-graph', 'value'), Input('daily-county-dropdown-bar-graph', 'value')])
def update_graph2(selected_state, selected_county):
    """Return a graph

    Update county graph with selected state and county
    """
    cases = helper.Confirmed(selected_state)
    states.set_state(selected_state)

    cases.set_county(selected_county)
    trace1 = go.Bar(x=cases.get_dates_since_start(), y=cases.get_daily_county_cases(),
                        name='Cases')

    data = [trace1]
    county_graph = {'data': data,
                    'layout': go.Layout(
                        title='New Daily Confirmed Cases in ' + cases.get_county_name() + ' County, '
                              + cases.get_state_name(),
                        xaxis={'title': 'Date'},
                        yaxis={'title': 'Number of confirmed cases'})}

    return county_graph


@app.callback(
    Output('daily-county-dropdown-bar-graph', 'options'), [Input('daily-state-dropdown-bar-graph', 'value')])
def update_county_dropdown_menu(selected_state):
    """Return dropdown options for select-county

    Update county dropdown menu with counties in selected state
    """
    states.set_state(selected_state)
    return [{'label': k, 'value': k} for k in states.get_counties_in_state()]


@app.callback(
    Output('daily-county-dropdown-bar-graph', 'value'),
    [dash.dependencies.Input('daily-county-dropdown-bar-graph', 'options')])
def set_cities_value(available_options):
    return available_options[0]['value']


def get_layout():
    complete_layout = html.Div([
        nav,
        layout
    ])
    return complete_layout

