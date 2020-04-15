import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
from Plots import helper

# Load CSV files from Datasets folder
df_confirmed = pd.read_csv('../Datasets/time_series_covid19_confirmed_US_new.csv')
df_deaths = pd.read_csv('../Datasets/time_series_covid19_deaths_US.csv')

app = dash.Dash()

states = helper.States()
states.set_state("North Carolina")

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
            {'label': k, 'value': k} for k in states.get_state_index_code_keys()
        ],
        value='North Carolina'
    ),
    dcc.Graph(id='graph2'),

    dcc.Dropdown(
        id='select-county',
        options=[
            # {'label': k, 'value': k} for k in states.get_counties_in_state()
            # {'label': 'Orange', 'value': 'North Carolina'},

        ],
        value=states.get_counties_in_state()[0]
    )
])


@app.callback(Output('graph1', 'figure'),
              [Input('select-state', 'value')])
def update_graph1(selected_state):
    states.set_state(selected_state)

    # Preparing Data
    cases = helper.Confirmed(selected_state)

    #  State Graph
    trace1 = go.Scatter(x=cases.get_dates_since_start(), y=cases.get_total_state_cases_over_time(), mode='lines',
                        name='Cases')
    data = [trace1]
    state_graph = {'data': data,
                   'layout': go.Layout(
                       title='Total number of Confirmed Cases in ' + cases.get_state_name(),
                       xaxis={'title': 'Date'},
                       yaxis={'title': 'Number of confirmed cases'})}
    return state_graph


@app.callback(
    Output('graph2', 'figure'),
    [Input('select-state', 'value'), Input('select-county', 'value')])
def update_graph2(selected_state, selected_county):
    # County Graph
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
    states.set_state(selected_state)
    return [{'label': k, 'value': k} for k in states.get_counties_in_state()]


@app.callback(
    Output('select-county', 'value'),
    [dash.dependencies.Input('select-county', 'options')])
def set_cities_value(available_options):
    return available_options[0]['value']


if __name__ == '__main__':
    app.run_server(debug=False)
