import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from Plots import helper

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
    html.Div('Coronavirus COVID-19 State and County Daily Confirmed Cases', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Interactive Line chart', style={'color': '#df1e56'}),
    html.Div(
        'This chart represents the amount of daily confirmed cases reported each day'),
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
        options=[],
        value=states.get_counties_in_state()[0]
    ),
    html.Br(),
    html.Br()
])


@app.callback(Output('graph1', 'figure'),
              [Input('select-state', 'value')])
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
    Output('graph2', 'figure'),
    [Input('select-state', 'value'), Input('select-county', 'value')])
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


if __name__ == '__main__':
    app.run_server(debug=False)
