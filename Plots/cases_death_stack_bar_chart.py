import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

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
    html.Div('Coronavirus COVID-19 County Cases and Deaths', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Interactive Stack Bar chart', style={'color': '#df1e56'}),
    html.Div(
        'This chart represents the total of confirmed cases and deaths in the first 20 counties of selected state.'),
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
    )
])


@app.callback(Output('graph1', 'figure'),
              [Input('select-state', 'value')])
def update_figure(selected_state):
    date_d = date_for_graph
    date_c = date_for_graph + '20'

    filtered_df_confirmed = df_confirmed[df_confirmed['Province_State'] == selected_state]
    filtered_df_deaths = df_deaths[df_deaths['Province_State'] == selected_state]
    # Creating
    new_df_confirmed = filtered_df_confirmed.groupby(['Admin2'])[date_c].sum().reset_index()
    new_df_deaths = filtered_df_deaths.groupby(['Admin2'])[date_d].sum().reset_index()

    # Sorting values and select first 20 Counties
    new_df_confirmed = new_df_confirmed.sort_values(by=[date_c], ascending=[False]).head(10).reset_index()
    new_df_deaths = new_df_deaths.sort_values(by=[date_d], ascending=[False]).head(10).reset_index()

    # Preparing data
    trace1 = go.Bar(x=new_df_confirmed['Admin2'], y=new_df_confirmed[date_c], name='Confirmed',
                    marker={'color': '#CD7F32'})
    trace2 = go.Bar(x=new_df_deaths['Admin2'], y=new_df_deaths[date_d], name='Deaths', marker={'color': '#9EA0A1'})

    data = [trace1, trace2]
    return {'data': data,
            'layout': go.Layout(
                title='Total number of Confirmed Cases and Deaths by County as of {0}'.format(date_c),
                xaxis={'title': 'County'},
                yaxis={'title': 'Number of confirmed cases and deaths'})}


if __name__ == '__main__':
    app.run_server()
