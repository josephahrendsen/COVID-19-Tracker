import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go
from Plots import helper
from navbar import Navbar
from app import app

nav = Navbar()


states = helper.States()
states.set_state("North Carolina")

layout = html.Div(className='graph-layout', children=[
    # Layout for Line Graph
    html.H1(children='Cases of COVID-19 in Each State and County',
            style={
                'textAlign': 'center',
                'color': 'white'
            }
            ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Interactive Line chart', style={'color': 'white'}),
    html.Div('This chart represents the total number of confirmed cases in a state'),
    html.Div('Please select a state', style={'color': '#ef3e18'}),
    dcc.Dropdown(
        id='select-state',
        options=[
            {'label': k, 'value': k} for k in states.get_state_index_code_keys()
        ],
        value='North Carolina',
        style={'color': 'black'}
    ),
    dcc.Graph(id='graph1'),
    html.Br(),
    html.Div('This chart represents the total number of confirmed cases in a county'),
    html.Div('Please select a county', style={'color': '#ef3e18'}),
    dcc.Dropdown(
        id='select-county',
        options=[],
        value=states.get_counties_in_state()[0],
        style={'color': 'black'}
    ),
    dcc.Graph(id='graph2'),

    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),


    # Layout for Scatter Plot
    html.H3('Scatter Plot for COVID-19 Cases by County ', style={'color': 'white'}),
    html.Div(
        'This scatter plot represents the Corona Virus cases per county in a given State.'),
    html.Div('Please select a state', style={'color': '#ef3e18', 'margin': '10px'}),
    dcc.Dropdown(
        id='state-cases-scatter-plot-dropdown',
        options=[
            {'label': k, 'value': k} for k in states.get_state_index_code_keys()
        ],
        value='North Carolina',
        style={'color': 'black'}

    ),
    dcc.Graph(id='state-cases-scatter-plot')
])


# Line Graph
@app.callback(Output('graph1', 'figure'),
              [Input('select-state', 'value')])
def update_graph1(selected_state):
    """Return a graph

    Update state graph with selected state
    """
    states.set_state(selected_state)

    # Preparing Data
    cases = helper.Confirmed(selected_state)

    trace1 = go.Scatter(x=cases.get_dates_since_start(), y=cases.get_total_state_cases_over_time(), mode='lines',
                        name='Cases')
    data = [trace1]
    state_graph = {'data': data,
                   'layout': go.Layout(
                       title='Total number of Confirmed Cases in ' + cases.get_state_name(),
                       xaxis={'title': 'Date'},
                       yaxis={'title': 'Number of confirmed cases'}
                   )}
    return state_graph


@app.callback(
    Output('graph2', 'figure'),
    [Input('select-state', 'value'), Input('select-county', 'value')])
def update_graph2(selected_state, selected_county):
    """Return a graph

    Update county graph with selected state and county
    """
    cases = helper.Confirmed(selected_state)
    states.set_state(selected_state)

    cases.set_county(selected_county)
    trace1 = go.Scatter(x=cases.get_dates_since_start(), y=cases.get_county_cases_over_time(), mode='lines',
                        name='Cases')
    data = [trace1]
    county_graph = {'data': data,
                    'layout': go.Layout(
                        title='Total number of Confirmed Cases in ' + cases.get_county_name() + ' County, '
                              + cases.get_state_name(),
                        xaxis={'title': 'Date'},
                        yaxis={'title': 'Number of confirmed cases'})}

    return county_graph


@app.callback(
    Output('select-county', 'options'), [Input('select-state', 'value')])
def update_county_dropdown_menu(selected_state):
    """Return dropdown options for select-county

    Update county dropdown menu with counties in selected state
    """
    states.set_state(selected_state)
    return [{'label': k, 'value': k} for k in states.get_counties_in_state()]


@app.callback(
    Output('select-county', 'value'),
    [dash.dependencies.Input('select-county', 'options')])
def set_cities_value(available_options):
    return available_options[0]['value']


# Scatter Plot
@app.callback(Output('state-cases-scatter-plot', 'figure'),
              [Input('state-cases-scatter-plot-dropdown', 'value')])
def update_figure(selected_state):

    states.set_state(selected_state)

    cases = helper.Confirmed(selected_state)

    trace1 = go.Scatter(
        x=cases.get_all_counties_unsorted(),
        y=cases.get_all_counties_total_cases_unsorted(),
        text=cases.get_county_name(),
        mode='markers')

    data = [trace1]

    scatter_plot = {'data': data,
                   'layout': go.Layout(
                       title='Cases by County in ' + cases.get_state_name(),
                       xaxis={'title': 'County Name'},
                       yaxis={'title': 'Number of confirmed cases'})}

    return scatter_plot


def get_layout():
    complete_layout = html.Div([
        nav,
        layout
    ])
    return complete_layout
