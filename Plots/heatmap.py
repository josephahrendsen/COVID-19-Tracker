from urllib.request import urlopen
import json
import pandas as pd
from pandas import DataFrame
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import math
from app import app
from navbar import Navbar
from Plots import helper

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

cases = pd.read_csv("Datasets/time_series_covid19_confirmed_US.csv", dtype={"FIPS": str})
deaths = pd.read_csv("Datasets/time_series_covid19_deaths_US.csv", dtype={"FIPS": str})

nav = Navbar()

LATEST_DATE = helper.Confirmed("North Carolina").get_latest_data_date()  # state doesn't matter

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
            ratio = cases[LATEST_DATE][i] / (deaths['Population'][i] / 10000)
            rounded_ratio = math.ceil(ratio * 100) / 100
            ratios.append(rounded_ratio)
        else:
            ratios.append(0)
    return ratios


def calculate_death_ratio():
    ratios = []
    for i in range(deaths[LATEST_DATE].__len__()):
        if deaths['Population'][i] != 0:
            ratio = deaths[LATEST_DATE][i] / (deaths['Population'][i] / 10000)
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
                           range_color=(0, 100),
                           scope="usa",
                           labels={'Ratio': ''}
                          )
cases_heatmap.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

# Deaths Heatmap
deaths_heatmap = px.choropleth(death_ratios, geojson=counties, locations=FIPS, color='Ratio',
                           color_continuous_scale=colors,
                           range_color=(0, 10),
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

layout = html.Div([
    dcc.Dropdown(
            id='select-heatmap',
            options=[
                {'label': 'COVID-19 Confirmed Cases per 10,000 Population', 'value': '1'},
                {'label': 'COVID-19 Deaths per 10,000 Population', 'value': '2'},
                {'label': 'COVID-19 Deaths from Cases Ratio', 'value': '3'}
            ],
            value='1',
            style={'color': 'black', 'width': '500px'}
        ),
    #html.Div('This choropleth represents the percent of COVID-19 Cases resulting in death'),
    dcc.Graph(id='heatmap',style={'width': '900px'})
])


# @app.callback(Output('heatmap', 'figure'),
#               [Input('select-heatmap', 'value')])
# def update_heatmap(selected_heatmap):
#     if selected_heatmap == '1':
#         return cases_heatmap
#     elif selected_heatmap == '2':
#         return deaths_heatmap
#     elif selected_heatmap == '3':
#         return deaths_per_cases_heatmap
#
#     return cases_heatmap
#


def get_layout():
    complete_layout = html.Div([
        nav,
        layout
    ])
    return complete_layout


