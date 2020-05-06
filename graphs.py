import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import math
from urllib.request import urlopen
import json
import pandas as pd
from pandas import DataFrame
from navbar import Navbar
from app import app
from Plots import helper, state_county_death_line_chart, state_county_confirmed_line_chart
from Plots import daily_changes_bar_chart, us_cases, us_deaths
nav = Navbar()

states = helper.States()
states.set_state("North Carolina")

layout = html.Div(children=[
    html.H1("Analytics", className="page-header"),
    html.Div([
        html.Div([
            html.A("Total Cases in the United States", className="active", href='#us-cases'),
            html.A("Total Deaths in the United States", href='#us-deaths'),
            html.A("Total Cases by State and County", href='#total-cases-state-county'),
            html.A("Total Deaths by State and County", href='#total-deaths-state-county'),
            html.A("Daily Cases by State and County", href='#daily-changes'),
        ], className="vertical-menu"),

        html.Div([
            dcc.Dropdown(
                id='select-heatmap',
                options=[
                    {'label': 'COVID-19 Confirmed Cases per 100,000 Population', 'value': '1'},
                    {'label': 'COVID-19 Deaths per 100,000 Population', 'value': '2'},
                    {'label': 'COVID-19 Deaths from Cases Percentage', 'value': '3'}
                ],
                value='1',
                style={'color': 'black', 'width': '500px', 'font-family': 'muli',
                       'font-size': '18px'}
            ),
            dcc.Graph(id='heatmap', style={'width': '900px'})
        ], className="side-graph")
    ], className="wrapper"),
    us_cases.layout,
    html.Hr(),

    us_deaths.layout,
    html.Hr(),

    state_county_confirmed_line_chart.layout,
    html.Hr(),

    state_county_death_line_chart.line_chart_layout,
    state_county_death_line_chart.stack_bar_chart_layout,
    html.Hr(),

    daily_changes_bar_chart.layout,
    html.Div([
        html.A("Total Cases in the United States", className="bottom-link", href='#us-cases'),
        html.A("Total Deaths in the United States", className="bottom-link", href='#us-deaths'),
        html.A("Total Cases by State and County", className="bottom-link", href='#total-cases-state-county'),
        html.A("Total Deaths by State and County", className="bottom-link", href='#total-deaths-state-county'),
        html.A("Daily Cases by State and County", className="bottom-link", href='#daily-changes')
    ], className="bottom-div")

])


# Heatmap code
LATEST_DATE = helper.Confirmed("North Carolina").get_latest_data_date()  # state doesn't matter
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

cases = pd.read_csv("Datasets/time_series_covid19_confirmed_US.csv", dtype={"FIPS": str})
deaths = pd.read_csv("Datasets/time_series_covid19_deaths_US.csv", dtype={"FIPS": str})
date_for_graph = helper.Confirmed("North Carolina").get_latest_data_date()
df_confirmed = pd.read_csv('Datasets/time_series_covid19_confirmed_US.csv')
df_deaths = pd.read_csv('Datasets/time_series_covid19_deaths_US.csv')

FIPS = []
# Remove extra zeroes from FIPS
for code in deaths['FIPS']:
    code = str(code)
    split_num = code.split(".", 1)
    FIPS.append(split_num[0].zfill(5))


def calculate_cases_ratio():
    ratios = []
    for i in range(deaths[LATEST_DATE].__len__()):
        if deaths['Population'][i] != 0:
            ratio = cases[LATEST_DATE][i] / (deaths['Population'][i] / 100000)
            rounded_ratio = math.ceil(ratio * 100) / 100
            ratios.append(rounded_ratio)
        else:
            ratios.append(0)
    return ratios


def calculate_death_ratio():
    ratios = []
    for i in range(deaths[LATEST_DATE].__len__()):
        if deaths['Population'][i] != 0:
            ratio = deaths[LATEST_DATE][i] / (deaths['Population'][i] / 100000)
            rounded_ratio = math.ceil(ratio * 100) / 100
            ratios.append(rounded_ratio)
        else:
            ratios.append(0)
    return ratios


def calculate_death_to_cases_ratio():
    ratios = []
    for i in range(deaths[LATEST_DATE].__len__()):
        if cases[LATEST_DATE][i] != 0:
            ratio = (deaths[LATEST_DATE][i] / cases[LATEST_DATE][i]) * 100
            rounded_ratio = math.ceil(ratio * 100) / 100
            ratios.append(rounded_ratio)
        else:
            ratios.append(0)
    return ratios


# Convert lists to data frames
cases_ratios = DataFrame(calculate_cases_ratio(), columns=['Ratio'])
death_ratios = DataFrame(calculate_death_ratio(), columns=['Ratio'])
deaths_to_cases_ratio = DataFrame(calculate_death_to_cases_ratio(), columns=['Ratio'])

colors = ["#F9F9F5", "#FAFAE6", "#FCFCCB", "#FCFCAE", "#FCF1AE", "#FCEA7D", "#FCD97D",
          "#FCCE7D", "#FCC07D", "#FEB562", "#F9A648", "#F98E48", "#FD8739", "#FE7519",
          "#FE5E19", "#FA520A", "#FA2B0A", "#9B1803", "#861604", "#651104", "#570303", ]

cases_heatmap = px.choropleth(cases_ratios, geojson=counties, locations=FIPS, color='Ratio',
                           color_continuous_scale=colors,
                           range_color=(0, 1000),
                           scope="usa",
                           labels={'Ratio': ''}
                          )
cases_heatmap.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

# Deaths Heatmap
deaths_heatmap = px.choropleth(death_ratios, geojson=counties, locations=FIPS, color='Ratio',
                           color_continuous_scale=colors,
                           range_color=(0, 100),
                           scope="usa",
                           labels={'Ratio': ''}
                          )
deaths_heatmap.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})


# Deaths per cases Heatmap
deaths_per_cases_heatmap = px.choropleth(deaths_to_cases_ratio, geojson=counties, locations=FIPS, color='Ratio',
                                         color_continuous_scale=colors,
                                         range_color=(0, 15),
                                         scope="usa",
                                         labels={'Ratio': ''}
                                         )
deaths_per_cases_heatmap.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

@app.callback(Output('heatmap', 'figure'),
              [Input('select-heatmap', 'value')])
def update_heatmap(selected_heatmap):
    if selected_heatmap == '1':
        return cases_heatmap
    elif selected_heatmap == '2':
        return deaths_heatmap
    elif selected_heatmap == '3':
        return deaths_per_cases_heatmap

    return cases_heatmap

# External Callbacks_________________________________________________________________________________________________


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

def Graphs():
    app_layout = html.Div([
        nav,
        layout
    ])

    return app_layout
