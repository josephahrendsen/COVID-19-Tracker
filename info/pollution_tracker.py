import dash_html_components as html

from navbar import Navbar

nav = Navbar()

layout = html.Div(style={'fontSize': '22px', 'margin-left': '100px', 'margin-right': '100px'}, children=[
    html.H1("Pollution Tracker", className="page-header"),
    html.P("Sadly after much consideration the pollution tracker was ultimately scrapped due to the inability to find any good .csv files with decent data on pollution levels. This paper is only here to explain what we would have done if we would’ve found a decent .csv file with the relevant data."),
    html.P("The tracker would’ve used a line graph with one line to display average 2019 carbon monoxide and dioxide levels around several major US cities like Chicago, New York, and Los Angeles., and another line showing the average levels during the outbreak.  This city would have been selected by a drop down menu just like all other charts in our project."),
    html.P("The link in question shows another way we could have done it with two heatmaps showing average air pollution levels on January 20, 2020 vs March 20, 2020. It is very easy to see that around major cities like New York, levels of air pollutants have dropped a considerable amount."),
    html.Br(),
    html.A("Link to external interactive pollution graph", href="https://earther.gizmodo.com/coronavirus-slashes-global-air-pollution-interactive-m-1842473790")
    ],
)


def get_layout():
    complete_layout = html.Div([
        nav,
        layout
    ])
    return complete_layout
