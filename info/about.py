import dash_html_components as html
import dash_core_components as dcc
from navbar import Navbar

nav = Navbar()

layout = html.Div(style={'fontSize': '22px', 'margin-left': '100px', 'margin-right': '100px'}, children=[
    html.H1("About Our Site", className="page-header"),
    html.H2("Inspiration", style={'text-decoration': 'underline'}),
    html.P('We decided for our final project to be focused around the novel Coronavirus. We have never faced anything like this in modern history and America has developed the most cases in the world. Even with thousands of people dying, there are still so many people who do not take this seriously. The idea behind this project is to show Americans how fast the COVID-19 virus spreads though easy-to-understand visuals.'),

    html.H2("Overview", style={'text-decoration': 'underline'}),
    html.P("This site is designed to show multiple different tabs as well as graphs with Coronavirus related data. It is split into four main tabs; Analytics, Effects on the United States, what to do, and the current About page."),

    html.H2("How it works", style={'text-decoration': 'underline'}),
    html.P("On the Analytics page, you will find multiple categories of graphs to choose from. Once you make a selection you will be provided with an appropriate graph or graphs with updated data. The majority of the graphs are interactive, allowing you to select from either state or county options and provides data accordingly."),
    html.P("The Effects on the United States page is a summary of what is going on in our country due to the COVID-19 virus. It is separated into two sections, unemployment and pollution. Also provided are links to external graphs where you can see relevant data to the section you are under."),
    html.P("The what to do page simply explains the best ways to stay safe and go about living during this pandemic. The data for the above two pages is gathered from John Hopkins GitHub where it is updated daily, as well as from the U.S. Bureau of Labor Statistics. Our data is from reputable sources and will provide accurate information to our site’s users."),

    html.H2("Conclusion", style={'text-decoration': 'underline'}),
    html.P("We hope that our site will provide value to Americans and allow them to remain informed on current issues surrounding the COVID-19 pandemic. By providing visualizations and information on the number of people infected in your area, you will be able to get a grasp of how serious this virus is. If you have any questions or feedback, please reach out to one of our developers at the emails provided. Stay safe!"),
    html.Br(),

    html.H2("Contact us:", style={'text-align': 'center'}),
    html.Br(),
    html.Div([
        html.Div([
            html.Img(className='headshot', src='../assets/joseph_headshot1.jpg'),
            html.P("Joseph Ahrendsen", className='about-subtext'),
            html.P("jahrends@uncc.edu", className='about-subtext')
        ], className='button-wrapper'),
        html.Div([
            html.Img(className='headshot', src='../assets/austin_headshot.jpg', style={'margin-left': '100px'}),
            html.P("Austin Brown", className='about-subtext', style={'margin-left': '100px'}),
            html.P("abrow322@uncc.edu", className='about-subtext', style={'margin-left': '100px'})
        ], className='button-wrapper'),
        html.Div([
            html.Img(className='headshot', src='../assets/cameron_headshot.jpg', style={'margin-left': '100px'}),
            html.P("Cameron Nixon", className='about-subtext', style={'margin-left': '100px'}),
            html.P("cnixon14@uncc.edu", className='about-subtext', style={'margin-left': '100px'})
        ], className='button-wrapper'),
        html.Div([
            html.Img(className='headshot', src='../assets/andrew_headshot.jpg', style={'margin-left': '100px'}),
            html.P("Kaleb Schimmel", className='about-subtext', style={'margin-left': '100px'}),
            html.P("kschimme@uncc.edu", className='about-subtext', style={'margin-left': '100px'})
        ], className='button-wrapper'),
    ], className='home-page-wrapper')
    ],
)


def get_layout():
    complete_layout = html.Div([
        nav,
        layout
    ])
    return complete_layout
