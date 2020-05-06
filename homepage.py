import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from navbar import Navbar
from app import app

nav = Navbar()

layout = html.Div(children=[
    html.Div([
        html.Div([
            html.Div([
                html.P("Analytics", className='subtext'),
                dcc.Link(html.Button(className='home-page-button',
                                     style={'background-image': 'url(../assets/analytics_icon.png'}
                                     ), href='/graphs'),
            ], className='button-wrapper'),
            html.Div([
                html.P("Effects on US", className='subtext', style={'margin-left': '100px'}),
                dcc.Link(html.Button(className='home-page-button',
                                     style={'background-image': 'url(../assets/flag_icon.png', 'margin-left': '100px'}
                                     ), href='/#'),
            ], className='button-wrapper'),

            html.H1("COVID-19 Tracker", className="home-page-title"),

            html.Div([
                dcc.Link(html.Button(className='home-page-button',
                                     style={'background-image': 'url(../assets/checklist_icon.png'}
                                     ), href='/info/what_to_do'),
                html.P("What to Do", className='subtext')
            ], className='button-wrapper'),
            html.Div([
                dcc.Link(html.Button(className='home-page-button',
                                     style={'background-image': 'url(../assets/about_icon.png', 'margin-left': '100px'}
                                     ), href='/info/about'),
                html.P("About", className='subtext', style={'margin-left': '100px'}),
            ], className='button-wrapper'),
        ], className='home-page-wrapper')
    ], className='full-home-page'),
])


def Homepage():
    app_layout = html.Div([
        nav,
        layout
    ], style={'background-image': 'url(../assets/background.png', 'background-size': 'cover', 'height': '900px'})

    return app_layout
