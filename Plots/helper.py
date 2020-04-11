import pandas as pd
import calendar
from datetime import date, timedelta

# Create calendar object
cal = calendar.Calendar()

# Load CSV file from Datasets folder
df_cases = pd.read_csv('../Datasets/time_series_covid19_confirmed_US.csv')
df_deaths = pd.read_csv('../Datasets/time_series_covid19_deaths_US.csv')


class Confirmed:
    df_state = 0
    df_county = 0
    county_index_num = 0
    state = ""
    county = ""
    days = []
    start_data_date = date(2020, 3, 1).strftime("%#m/%#d/%Y")
    latest_data_date = date(2020, 4, 6).strftime("%#m/%#d/%Y")

    def __init__(self, state):
        self.state = state
        self.get_dates_since_start()

    def find_state(self):
        """ Return the correct state data if it exists (Data frame object) """
        is_state = df_cases['Province_State'] == self.state  # Assign true value to x state
        self.df_state = df_cases[is_state]  # Filter all data of x state
        return self.df_state

    def get_state_name(self):
        return self.state

    def set_county(self, county):
        self.county = county
        self.find_county()

    def find_county(self):
        """ Return the correct county data if it exists (Data frame object) """
        is_county = (df_cases['Admin2'] == self.county) & (df_cases['Province_State'] == self.state)  # Assign true value to x county
        self.df_county = df_cases[is_county]  # Filter all data of x county
        self.county_index_num = self.df_county.loc[self.df_county['Admin2'] == self.county].index[0]  # Get index of correct county
        return self.df_county

    def get_county_name(self):
        """Return name of a county (str)"""
        return self.county

    def get_county_cases_over_time(self):
        confirmed = []  # Create list of confirmed cases
        for i in range(len(self.get_days())):
            # add to confirmed list; formatted as [column][row]
            confirmed.append(self.df_county[self.days[i]][self.get_county_index()])
        return confirmed

    def get_county_index(self):
        return self.county_index_num

    def get_latest_data_date(self):
        return self.latest_data_date

    def get_total_state_cases(self):
        filtered_df_confirmed = df_cases[df_cases['Province_State'] == "North Carolina"]
        new_df_confirmed = filtered_df_confirmed.groupby(['Admin2'])[self.get_latest_data_date()].sum().reset_index()
        new_df_confirmed = new_df_confirmed.sort_values(by=[self.get_latest_data_date()], ascending=[False]).reset_index()

        case_total = 0
        for i in range(len(new_df_confirmed)):
            case_total += new_df_confirmed[self.get_latest_data_date()][i]
        return case_total

    def get_all_counties(self):
        filtered_df_confirmed = df_cases[df_cases['Province_State'] == self.state]
        new_df_confirmed = filtered_df_confirmed.groupby(['Admin2'])[self.get_latest_data_date()].sum().reset_index()
        new_df_confirmed = new_df_confirmed.sort_values(by=[self.get_latest_data_date()], ascending=[False]).reset_index()
        return new_df_confirmed['Admin2']

    def get_all_counties_total_cases(self):
        filtered_df_confirmed = df_cases[df_cases['Province_State'] == self.state]
        new_df_confirmed = filtered_df_confirmed.groupby(['Admin2'])[self.get_latest_data_date()].sum().reset_index()
        new_df_confirmed = new_df_confirmed.sort_values(by=[self.get_latest_data_date()], ascending=[False]).reset_index()
        return new_df_confirmed[self.get_latest_data_date()]

    def get_dates_since_start(self):
        days = []
        start_data_date = date(2020, 3, 1)
        latest_data_date = date(2020, 4, 6)
        delta = timedelta(days=1)
        while start_data_date <= latest_data_date:
            days.append(start_data_date.strftime("%#m/%#d/%Y"))  # Add dates to days list
            start_data_date += delta
        self.days = days
        return days

    def get_days(self):
        return self.days


'''
class CountyConfirmed:
    """A class used to represent data in the time_series_covid19_confirmed_US.csv

    Attributes
    ----------
    df_county : Data Frame object
        the data contained in a county
    county_row : int
        the specific index associated with a county
        """

    df_county = 0
    county = ""  # Must set to use county methods
    state = ""
    county_index = 0

    def __init__(self, county, state):
        self.county = county
        self.state = state
        self.find_county()

    def get_state_name(self):
        return self.state

    def find_county(self):
        """ Return the correct county data if it exists (Data frame object) """
        is_county = (df_cases['Admin2'] == self.county) & (df_cases['Province_State'] == self.state)  # Assign true value to x county
        self.df_county = df_cases[is_county]  # Filter all data of x county
        return self.df_county

    def get_county_name(self):
        """Return name of a county (str)"""
        # self.county = self.df_county['Admin2'][self.get_county_index()]
        return self.county

    def get_county_index(self):
        self.county_index = self.df_county.loc[self.df_county['Admin2'] == self.county].index[0]  # Get index of correct county
        return self.county_index

'''