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


# df_county_obj = find_county("Mecklenburg", "North Carolina")  # Get data for a county
df_county_obj = find_county("Orange", "North Carolina")  # Get data for a county
