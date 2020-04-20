import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


def Navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Analytics", href="/graphs"), style={'margin-right': '15px'}),
            dbc.NavItem(dbc.NavLink("National Effects", href="/#"), style={'margin-right': '15px'}),
            dbc.NavItem(dbc.NavLink("What to Do", href="/info/what_to_do"), style={'margin-right': '15px'}),
            dbc.NavItem(dbc.NavLink("About", href="/info/about"), style={'margin-right': '15px'}),
            dbc.NavItem(dbc.NavLink("Data Source", href="https://github.com/CSSEGISandData/COVID-19"))
        ],

        brand="Home",
        brand_href="/home",
        #sticky="top",
        style={'margin-bottom': '25px', 'font-family': 'mari', 'fontSize': '18px'}
    )
    return navbar

