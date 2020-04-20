import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from navbar import Navbar

nav = Navbar()

layout = html.Div(children=[
    html.H1("Analytics", className="page-header"),
    html.Div([
        html.A("Total Cases in the United States", className="active", href='/Plots/us_cases'),
        html.A("Total Deaths in the United States", href='/Plots/us_deaths'),
        html.A("Total Cases by State and County", href='/Plots/state_county_confirmed_line_chart'),
        html.A("Total Deaths by State and County", href='/Plots/state_county_death_line_chart'),
        html.A("Daily Cases by State and County", href='/Plots/daily_changes_bar_chart'),
        ], className="vertical-menu"),
    ],
    )


def Graphs():
    app_layout = html.Div([
        nav,
        layout
    ])

    return app_layout
