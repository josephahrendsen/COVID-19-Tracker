import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from Plots import stocks
from info import pollution_tracker, unemployment
from navbar import Navbar
from app import app

nav = Navbar()

layout = html.Div(children=[
    html.H1("Effects on the United States", className="page-header"),
    html.Div([
        stocks.layout,
        html.Hr(),

        unemployment.layout,
        html.Hr(),

        pollution_tracker.layout
    ]),
])


def Effects():
    app_layout = html.Div([
        nav,
        layout
    ])

    return app_layout
