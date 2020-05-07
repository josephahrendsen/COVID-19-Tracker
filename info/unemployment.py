import dash_html_components as html

from navbar import Navbar

nav = Navbar()

layout = html.Div(style={'fontSize': '22px', 'margin-left': '100px', 'margin-right': '100px'}, children=[
    html.H1("Unemployment Due to COVID-19 Virus", className="page-header"),
    html.A("Click Here for Civilian Unemployment Rate Graph", href='https://www.bls.gov/charts/employment-situation/civilian-unemployment-rate.htm'),
    html.P("This link is provided by The U.S. Bureau of Labor Statistics"),
    html.Br(),
    html.P("The unemployment rate in the United States has risen to 4.4 percent as of March 2020, which is the highest it has been since 2017. COVID-19 has taken its effect on our nation’s economy and is resulting in many Americans losing their jobs and filing for unemployment. In the three weeks leading up to April, over 17 million Americans filed for unemployment. Due to this, congress has passed a $2.2 trillion economic rescue package which provides extra payment to those unemployed for the first four months. This will try to help those in need get by until the virus dies down."),
    html.P("Most states by now have initiated a Stay-At-Home order, which requires all residents to stay isolated at their houses except for necessary shopping like groceries and people with essential jobs. While these essential workers are not having to file for unemployment, they are exposing themselves to potentially getting the virus and helping it spread. It is extremely difficult for the government to find a balance between keeping its citizens safe and keeping the economy from crashing. If no one was an essential worker, then there would be no internal cashflow which could send us into a depression, and if everyone was allowed to travel freely, the majority of the public would put at risk. Until the virus stops spreading, our nation will continue to struggle, so the best thing anyone can do is practice social distancing and follow the instructions provided by your state and federal government. ")
    ],
)


def get_layout():
    complete_layout = html.Div([
        nav,
        layout
    ])
    return complete_layout
