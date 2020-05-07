import dash_html_components as html

from navbar import Navbar

nav = Navbar()
# with open('/What_To_Do.txt', 'r') as myfile:
#     data = myfile.read()

layout = html.Div(style={'fontSize': '22px', 'margin-left': '100px', 'margin-right': '100px'}, children=[
    html.H1("What to Do", className="page-header"),
    html.P("Follow these five basic steps to avoid exposing yourself or others to the novel COVID-19 virus:"),
    html.P("1) Clean your hands often! Wash for at least 20 seconds. Hand sanitizer containing at least 60% alcohol is a suitable alternative."),
    html.P("2) Avoid close contact! Practice social distancing in public by maintaining at least a 6-feet-distance from strangers."),
    html.P("3) Cover your face with a cloth mask in public! Those without symptoms can still be contagious. Limit exposure from sneezing, coughing, and touching the face with a cover. "),
    html.P("4) Cover your coughs and sneezes! Residue on tissues or your hands from coughing and sneezing can get transported into the public if they are not scrubbed off. Hygiene guidelines like these should be followed even in private; infecting surfaces and the air is more difficult then stopping the particles from spreading in the first place."),
    html.P("5) Clean and disinfect! Residue can accumulate on surfaces like desks, countertops, and doorknobs. Any surface with regular human contact could be cleaned regularly to mitigate spread. "),
    html.A("Visit the Center for Disease Control website for more information on the epidemic:", href="https://www.cdc.gov/coronavirus/2019-ncov/index.html")
    ],
)


def get_layout():
    complete_layout = html.Div([
        nav,
        layout
    ])
    return complete_layout
