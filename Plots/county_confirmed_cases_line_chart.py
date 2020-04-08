import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go
import calendar
from datetime import date, timedelta

# Create calendar object
cal = calendar.Calendar()

# Load CSV file from Datasets folder
df = pd.read_csv('../Datasets/time_series_covid19_confirmed_US.csv')


class DfCounty:
    """A class used to represent data contained in a county
    
    Attributes
    ----------
    df_county : Data Frame object
        the data contained in a county
    county_row : int
        the specific index associated with a county
        """

    def __init__(self, df_county, county_index):
        self.df_county = df_county
        self.county_row = county_index


def find_county(county, state):
    """ Return the correct county data if it exists (DfCounty object) """
    is_county = (df['Admin2'] == county) & (df['Province_State'] == state)
    df_county = df[is_county]
    index_num = df_county.loc[df_county['Admin2'] == county].index[0]  # Get index of correct county
    return DfCounty(df_county, index_num)


def get_county_name():
    """Return name of a county (str)"""
    return df_county_obj.df_county['Admin2'][df_county_obj.county_row]


days = []  # Create list of all days
start_date = date(2020, 3, 1)
end_date = date(2020, 4, 6)
delta = timedelta(days=1)
while start_date <= end_date:
    days.append(start_date.strftime("%#m/%#d/%Y"))  # Add dates to days list
    start_date += delta

# df_county_obj = find_county("Mecklenburg", "North Carolina")  # Get data for a county
df_county_obj = find_county("Orange", "North Carolina")  # Get data for a county

confirmed = []  # Create list of confirmed cases
for i in range(len(days)):
    # add to confirmed list; formatted as [column][row]
    confirmed.append(df_county_obj.df_county[days[i]][df_county_obj.county_row])

# Preparing Data
trace1 = go.Scatter(x=days, y=confirmed, mode='lines', name='Cases')
data = [trace1]

# Preparing Layout
layout = go.Layout(title=("COVID-19 Confirmed Cases for " + get_county_name() + " County"),
                   xaxis_title="Day", yaxis_title="Confirmed Cases")

# Plot the figure and save to HTML file
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='county_confirmed_cases_line_chart.html')
