import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from navbar import Navbar
from app import app

nav = Navbar()

layout = html.Div(className='full-home-page', children=[
    html.H1("COVID-19 Tracker",
            style={
                'textAlign': 'center',
                'color': 'white',
                'font-size': '72px',
                'margin-top': '25px',
                'margin-bottom': '50px'
            }
            ),
    html.Div([
        html.Div(className='home-page-div', children=[
            html.A('Analytics', href='/graphs', style={'color': 'white'})
        ]),
        html.Div(className='home-page-div', children=[
            html.A('Effects on the United States', href='/#', style={'color': 'white'})
        ]),
        html.Div(className='home-page-div', children=[
            html.A('What to do', href='/#', style={'color': 'white'})
        ]),
        html.Div(className='home-page-div', children=[
            html.A('About', href='/#', style={'color': 'white'})
        ]),
        ], style={'marginBottom': 50, 'marginTop': 25, 'width': '1000px',
                  'border': '2px solid black', 'overflow': 'hidden', 'margin': '0 auto'}
        )
        # html.Div([
        #     dcc.Link(html.Button("Total Cases in the United States", className='button'),
        #              href='/Plots/state_county_confirmed_line_chart'),
        #     dcc.Link(html.Button("Total Deaths in the United States", className='button'),
        #              href='/Plots/state_county_confirmed_line_chart'),
        #     dcc.Link(html.Button("Total Cases by State and County", className='button'),
        #              href='/Plots/state_county_confirmed_line_chart'),
        #     dcc.Link(html.Button("Total Deaths by State and County", className='button'),
        #              href='/Plots/state_county_confirmed_line_chart'),
        #     dcc.Link(html.Button("Daily Cases by State and County", className='button'),
        #              href='/Plots/state_county_confirmed_line_chart')
        #     ], style={'marginBottom': 50, 'marginTop': 25, 'width': '1200px', 'height' : '1000px',
        #           'border': '1px solid black', 'overflow': 'hidden', 'margin': '0 auto'}),
        #],
])


def Homepage():
    app_layout = html.Div([
        nav,
        layout
    ])

    return app_layout
