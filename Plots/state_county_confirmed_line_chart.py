import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
from Plots import helper

# TODO
"""
Make county selection limited to counties in selected state
Don't allow invalid input
"""

# Most recent date on the csv's in Datasets
date_for_graph = '4/6/20'

# Load CSV files from Datasets folder
df_confirmed = pd.read_csv('../Datasets/time_series_covid19_confirmed_US.csv')
df_deaths = pd.read_csv('../Datasets/time_series_covid19_deaths_US.csv')

app = dash.Dash()

# Layout
app.layout = html.Div(children=[
    html.H1(children='COVID-19 Dash',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div('Web dashboard for Coronavirus Data', style={'textAlign': 'center'}),
    html.Div('Coronavirus COVID-19 State and County Cases', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Interactive Line chart', style={'color': '#df1e56'}),
    html.Div(
        'This chart represents the total of confirmed cases in a state'),
    dcc.Graph(id='graph1'),
    html.Div('Please select a state', style={'color': '#ef3e18', 'margin': '10px'}),
    dcc.Dropdown(
        id='select-state',
        options=[
            {'label': 'North Carolina', 'value': 'North Carolina'},
            {'label': 'South Carolina', 'value': 'South Carolina'},
            {'label': 'Georgia', 'value': 'Georgia'},
            {'label': 'New York', 'value': 'New York'},
            {'label': 'California', 'value': 'California'},
            {'label': 'Texas', 'value': 'Texas'}
        ],
        value='North Carolina'
    ),
    dcc.Graph(id='graph2'),

    dcc.Dropdown(
        id='select-county',
        options=[
            {'label': 'Orange', 'value': 'Orange'},
            {'label': 'Mecklenburg', 'value': 'Mecklenburg'},
        ],
        value='Orange'
    )

])


@app.callback([Output('graph1', 'figure'), Output('graph2', 'figure')],
                     [Input('select-state', 'value'), Input('select-county', 'value')])
def update_figure(selected_state, selected_county):

    # Preparing Data
    cases = helper.Confirmed(selected_state)

    #  State Graph
    trace1 = go.Scatter(x=cases.get_dates_since_start(), y=cases.get_total_state_cases_over_time(), mode='lines',
                        name='Cases')
    data = [trace1]
    state_graph = {'data': data,
            'layout': go.Layout(
                title='Total number of Confirmed Cases and Deaths by County in ' + cases.get_state_name(),
                xaxis={'title': 'Date'},
                yaxis={'title': 'Number of confirmed cases and deaths'})}

    #  County Graph
    cases.set_county(selected_county)  # Select county
    trace1 = go.Scatter(x=cases.get_dates_since_start(), y=cases.get_county_cases_over_time(), mode='lines',
                        name='Cases')
    data = [trace1]
    county_graph = {'data': data,
                   'layout': go.Layout(
                       title='Total number of Confirmed Cases in ' + cases.get_county_name() + ' County',
                       xaxis={'title': 'Date'},
                       yaxis={'title': 'Number of confirmed cases and deaths'})}

    return state_graph, county_graph


if __name__ == '__main__':
    app.run_server(debug=False)
