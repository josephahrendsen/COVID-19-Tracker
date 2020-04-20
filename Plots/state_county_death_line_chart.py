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
date_for_graph = '4/19/20'

# Line Chart Layout
line_chart_layout = html.Div(className='graph-layout', children=[
    # Layout for Line Graph
    html.H1(children='Deaths from COVID-19 in Each State and County',
            style={
                'textAlign': 'center',
                'color': 'white'
            }
            ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Interactive Line chart', style={'color': 'white'}),
    html.Div('This chart represents the total number of confirmed deaths in a state'),
    html.Div('Please select a state', style={'color': '#ef3e18'}),
    dcc.Dropdown(
        id='state-death-line-chart-dropdown',
        options=[
            {'label': k, 'value': k} for k in states.get_state_index_code_keys()
        ],
        value='North Carolina',
        style={'color': 'black'}
    ),
    dcc.Graph(id='state-death-line-chart'),

    html.Br(),

    dcc.Dropdown(
        id='county-death-line-chart-dropdown',
        options=[],
        value=states.get_counties_in_state()[0],
        style={'color': 'black'}

    ),
    dcc.Graph(id='county-death-line-chart'),

    html.Br(),
    html.Br()
])


df_confirmed = pd.read_csv('Datasets/time_series_covid19_confirmed_US.csv')
df_deaths = pd.read_csv('Datasets/time_series_covid19_deaths_US.csv')

# Stack Bar Chart Layout
stack_bar_chart_layout = html.Div(className='graph-layout', children=[
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Interactive Stack Bar chart', style={'color': 'white'}),
    html.Div(
        'This chart represents the total of confirmed cases and deaths in the first 20 counties of selected state.'),
    html.Div('Please select a state', style={'color': '#ef3e18', 'margin': '10px'}),
    dcc.Dropdown(
        id='cases-death-stack-bar-chart-state-dropdown',
        options=[
            {'label': k, 'value': k} for k in states.get_state_index_code_keys()
        ],
        value='North Carolina'
    ),
    dcc.Graph(id='cases-death-stack-bar-chart-state-graph'),
])


@app.callback(Output('state-death-line-chart', 'figure'),
              [Input('state-death-line-chart-dropdown', 'value')])
def update_graph1(selected_state):
    """Return a graph

    Update state graph with selected state
    """
    states.set_state(selected_state)

    # Preparing Data
    deaths = helper.Deaths(selected_state)

    trace1 = go.Scatter(x=deaths.get_dates_since_start(), y=deaths.get_total_state_deaths_over_time(), mode='lines',
                        name='Cases')
    data = [trace1]
    state_graph = {'data': data,
                   'layout': go.Layout(
                       title='Total Number of Deaths in ' + deaths.get_state_name(),
                       xaxis={'title': 'Date'},
                       yaxis={'title': 'Number of confirmed deaths'})}
    return state_graph


@app.callback(
    Output('county-death-line-chart', 'figure'),
    [Input('state-death-line-chart-dropdown', 'value'), Input('county-death-line-chart-dropdown', 'value')])
def update_graph2(selected_state, selected_county):
    """Return a graph

    Update county graph with selected state and county
    """
    deaths = helper.Deaths(selected_state)
    states.set_state(selected_state)

    deaths.set_county(selected_county)
    trace1 = go.Scatter(x=deaths.get_dates_since_start(), y=deaths.get_county_deaths_over_time(), mode='lines',
                        name='Cases')
    data = [trace1]
    county_graph = {'data': data,
                    'layout': go.Layout(
                        title='Total number of Deaths in ' + deaths.get_county_name() + ' County, '
                              + deaths.get_state_name(),
                        xaxis={'title': 'Date'},
                        yaxis={'title': 'Number of confirmed deaths'})}

    return county_graph


@app.callback(
    Output('county-death-line-chart-dropdown', 'options'), [Input('state-death-line-chart-dropdown', 'value')])
def update_county_dropdown_menu(selected_state):
    """Return dropdown options for select-county

    Update county dropdown menu with counties in selected state
    """
    states.set_state(selected_state)
    return [{'label': k, 'value': k} for k in states.get_counties_in_state()]


@app.callback(
    Output('county-death-line-chart-dropdown', 'value'),
    [dash.dependencies.Input('county-death-line-chart-dropdown', 'options')])
def set_cities_value(available_options):
    return available_options[0]['value']


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
        line_chart_layout,
        stack_bar_chart_layout
    ])
    return complete_layout
