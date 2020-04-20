import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from homepage import Homepage
from graphs import Graphs
from Plots import state_county_confirmed_line_chart, daily_changes_bar_chart
from Plots import state_county_death_line_chart
from Plots import us_cases, us_deaths

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/Plots/state_county_confirmed_line_chart':
        return state_county_confirmed_line_chart.get_layout()
    elif pathname == '/Plots/daily_changes_bar_chart':
        return daily_changes_bar_chart.get_layout()
    elif pathname == '/Plots/us_cases':
        return us_cases.get_layout()
    elif pathname == '/Plots/us_deaths':
        return us_deaths.get_layout()
    elif pathname == '/Plots/state_county_death_line_chart':
        return state_county_death_line_chart.get_layout()
    elif pathname == '/graphs':
        return Graphs()
    else:
        return Homepage()


if __name__ == '__main__':
    app.run_server(debug=True)
