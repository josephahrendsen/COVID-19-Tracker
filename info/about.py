import dash_html_components as html

from navbar import Navbar

nav = Navbar()
# with open('/about.txt', 'r') as myfile:
#     data = myfile.read()

layout = html.Div(style={'fontSize': '22px', 'margin-left': '100px', 'margin-right': '100px'}, children=[
    html.H1("About", className="page-header"),
    html.P("We decided for our final project to be focused around the novel Coronavirus. We have never faced anything like this in modern history and America has developed the most cases in the world. Even with thousands of people dying, there are still so many people who do not take this seriously. The idea behind this project is to show Americans how fast the COVID-19 virus spreads though easy-to-understand visuals. This site is designed to show multiple different tabs as well as graphs with Coronavirus related data. This data is gathered from John Hopkins GitHub, where it is updated daily which keeps our site up to date. Multiple of the charts are also interactive, letting you select the state and/or county depending on what information you are wanting to view. The Coronavirus is the first pandemic in over ten years and has shocked the world. It is one of the most contagious viruses and can spread extraordinarily fast. People most commonly affect are anyone 65 and older or anyone with high-risk-conditions such as chronic lung disease, asthma, heart conditions, etc. These people should take extra precautions when going into public spaces and should avoid any type of crowd. Everyone should follow the guidelines given by CDC to reduce the spreading of this disease and to flatten the curve.")
    ],
)


def get_layout():
    complete_layout = html.Div([
        nav,
        layout
    ])
    return complete_layout