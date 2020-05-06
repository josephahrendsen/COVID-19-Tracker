import dash_html_components as html

from navbar import Navbar

nav = Navbar()
# with open('/about.txt', 'r') as myfile:
#     data = myfile.rea

layout = html.Div(style={'fontSize': '22px', 'margin-left': '100px', 'margin-right': '100px'}, children=[
    html.H1("About our Site", className="page-header"),
    html.P('We decided for our final project to be focused around the novel Coronavirus. We have never faced anything like this in modern history and America has developed the most cases in the world. Even with thousands of people dying, there are still so many people who do not take this seriously. The idea behind this project is to show Americans how fast the COVID-19 virus spreads though easy-to-understand visuals.'),
    html.P("This site is designed to show multiple different tabs as well as graphs with Coronavirus related data. It is split into four main tabs; Analytics, Effects on the United States, what to do, and the current About page."),
    html.P("On the Analytics page, you will find multiple categories of graphs to choose from. Once you make a selection you will be provided with an appropriate graph or graphs with updated data. The majority of the graphs are interactive, allowing you to select from either state or county options and provides data accordingly."),
    html.P("The Effects on the United States page is a summary of what is going on in our country due to the COVID-19 virus. It is separated into two sections, unemployment and pollution. Also provided are links to external graphs where you can see relevant data to the section you are under."),
    html.P("The what to do page simply explains the best ways to stay safe and go about living during this pandemic. The data for the above two pages is gathered from John Hopkins GitHub where it is updated daily, as well as from the U.S. Bureau of Labor Statistics. Our data is from reputable sources and will provide accurate information to our site’s users."),
    html.P("We hope that our site will provide value to Americans and allow them to remain informed on current issues surrounding the COVID-19 pandemic. By providing visualizations and information on the number of people infected in your area, you will be able to get a grasp of how serious this virus is. If you have any questions or feedback, please reach out to one of our developers at the emails provided. Stay safe!"),
    html.Br(),
    html.H2("Contact us:"),
    html.P("Austin Brown: Abrow322@uncc.edu"),
    html.P("Cameron Nixon: Cnixon14@uncc.edu"),
    html.P("Joseph Ahrendsen: Jahrends@uncc.edu"),
    html.P("Kaleb Schimmel: Kschimme@uncc.edu")
    ],
)


def get_layout():
    complete_layout = html.Div([
        nav,
        layout
    ])
    return complete_layout