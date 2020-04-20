import pandas as pd
import calendar
from datetime import date, timedelta

# Create calendar object
cal = calendar.Calendar()

# Load CSV file from Datasets folder
df_cases = pd.read_csv('Datasets/time_series_covid19_confirmed_US.csv')
df_deaths = pd.read_csv('Datasets/time_series_covid19_deaths_US.csv')


class Confirmed:
    """
    A class used to simplify creating graphs based on confirmed cases.

    ...

    Attributes
    ----------
    df_state : data frame object
        a formatted data frame containing data of a specified state
    df_county : data frame object
        a formatted data frame containing data of a specified county
    county_index_num : int
        the index number of a specified county in the dataset
    state : str
        the name of the specified state
    county : str
        the name of the specified county
    days : date[]
        list of dates used from dataset
    start_data_date : str
        start date date represented as a string
    latest_data_date: str
        latest date of data represented as a string
    """

    df_state = 0
    df_county = 0
    county_index_num = 0
    state = ""
    county = ""
    days = []
    start_data_date = 0
    latest_data_date = 0

    def __init__(self, state):
        self.state = state
        self.get_dates_since_start()
        self.find_state()

    def find_state(self):
        """ Return the correct state data if it exists (Data frame object) """
        is_state = df_cases['Province_State'] == self.state  # Assign true value to x state
        self.df_state = df_cases[is_state]  # Filter all data of x state
        return self.df_state

    def get_state_name(self):
        """ Accessor for state (str) """
        return self.state

    def set_county(self, county):
        """ Mutator for county """
        self.county = county
        self.find_county()

    def find_county(self):
        """ Return the correct county data if it exists (Data frame object) """
        is_county = (df_cases['Admin2'] == self.county) & (df_cases['Province_State'] == self.state)  # Assign true value to x county
        self.df_county = df_cases[is_county]  # Filter all data of x county
        self.county_index_num = self.df_county.loc[self.df_county['Admin2'] == self.county].index[0]  # Get index of correct county
        return self.df_county

    def get_county_name(self):
        """ Return name of a county (str) """
        return self.county

    def get_county_cases_over_time(self):
        """ Return list of daily confirmed cases for a county (int[]) """
        confirmed = []  # Create list of confirmed cases
        for i in range(len(self.get_days())):
            # add to confirmed list; formatted as [column][row]
            confirmed.append(self.df_county[self.days[i]][self.get_county_index()])
        return confirmed

    def get_county_index(self):
        """ Accessor for county_index_num (int) """
        return self.county_index_num

    def get_latest_data_date(self):
        """ Accessor for latest_data_date (date) """
        return self.latest_data_date

    def get_total_state_cases(self):
        """ Return total number of cases in a state (int) """
        filtered_df_confirmed = df_cases[df_cases['Province_State'] == self.state]
        new_df_confirmed = filtered_df_confirmed.groupby(['Admin2'])[self.get_latest_data_date()].sum().reset_index()
        new_df_confirmed = new_df_confirmed.sort_values(by=[self.get_latest_data_date()], ascending=[False]).reset_index()

        case_total = 0
        for i in range(len(new_df_confirmed)):
            case_total += new_df_confirmed[self.get_latest_data_date()][i]
        return case_total

    def get_total_state_cases_over_time(self):
        """ Return daily totals of confirmed cases each day since start in a state (int[]) """
        filtered_df_confirmed = df_cases[df_cases['Province_State'] == self.get_state_name()]
        filtered_df_confirmed = filtered_df_confirmed.reset_index()  # Reset indices
        num_of_counties = filtered_df_confirmed.__len__()
        confirmed = []
        for date in range(len(self.get_days())):
            county_daily_total = 0
            for county in range(num_of_counties):
                county_daily_total += filtered_df_confirmed[self.get_days()[date]][county]
            confirmed.append(county_daily_total)
        return confirmed

    def get_all_counties(self):
        """ Return all counties in a state sorted by highest to lowest number of confirmed cases """
        filtered_df_confirmed = df_cases[df_cases['Province_State'] == self.state]
        new_df_confirmed = filtered_df_confirmed.groupby(['Admin2'])[self.get_latest_data_date()].sum().reset_index()
        new_df_confirmed = new_df_confirmed.sort_values(by=[self.get_latest_data_date()], ascending=[False]).reset_index()
        return new_df_confirmed['Admin2']

    def get_all_counties_unsorted(self):
        """ Return all counties in a state unsorted """
        unfiltered_df_confirmed = df_cases[df_cases['Province_State'] == self.state]
        new_df_confirmed = unfiltered_df_confirmed.groupby(['Admin2'])[self.get_latest_data_date()].sum().reset_index()
        return new_df_confirmed['Admin2']

    def get_all_counties_total_cases(self):
        """ Return all counties current number of cases sorted highest to lowest (data frame object) """
        print(self.get_latest_data_date())
        filtered_df_confirmed = df_cases[df_cases['Province_State'] == self.state]
        new_df_confirmed = filtered_df_confirmed.groupby(['Admin2'])[self.get_latest_data_date()].sum().reset_index()
        new_df_confirmed = new_df_confirmed.sort_values(by=[self.get_latest_data_date()], ascending=[False]).reset_index()
        return new_df_confirmed[self.get_latest_data_date()]

    def get_all_counties_total_cases_unsorted(self):
        """ Return all counties current number of cases unsorted"""
        print(self.get_latest_data_date())
        unfiltered_df_confirmed = df_cases[df_cases['Province_State'] == self.state]
        new_df_confirmed = unfiltered_df_confirmed.groupby(['Admin2'])[self.get_latest_data_date()].sum().reset_index()
        return new_df_confirmed[self.get_latest_data_date()]

    def get_dates_since_start(self):
        """ Calculate which dates to use from datasets (date[]) """
        days = []
        start_data_date = date(2020, 3, 1)
        latest_data_date = date(2020, 4, 19)
        delta = timedelta(days=1)
        while start_data_date <= latest_data_date:
            days.append(start_data_date.strftime("%#m/%#d/%y"))  # Add dates to days list
            start_data_date += delta
        self.days = days
        self.start_data_date = date(2020, 3, 1).strftime("%#m/%#d/%y")
        self.latest_data_date = date(2020, 4, 19).strftime("%#m/%#d/%y")
        return days

    def get_days(self):
        """ Accessor for days (date[]) """
        return self.days

    def get_daily_state_cases(self):
        """ Return daily change in confirmed cases in a specified state """
        daily_cases = []
        count = 0
        state_cases = self.get_total_state_cases_over_time()  # Program runs faster when this is duplicated

        for i in state_cases:
            if count < state_cases.__len__() - 1:
                if state_cases[count+1] - state_cases[count] < 0:
                    daily_cases.append(0)
                else:
                    daily_cases.append(state_cases[count+1] - state_cases[count])
                count += 1
        return daily_cases

    def get_daily_county_cases(self):
        """ Return daily change in confirmed cases in a specified county """
        daily_cases = []
        count = 0
        county_cases = self.get_county_cases_over_time()

        for i in county_cases:
            if count < county_cases.__len__() - 1:
                if county_cases[count+1] - county_cases[count] < 0:
                    daily_cases.append(0)
                else:
                    daily_cases.append(county_cases[count+1] - county_cases[count])
                count += 1
        return daily_cases


class Deaths:
    """
    A class used to simplify creating graphs based on deaths.

    ...

    Attributes
    ----------
    df_state : data frame object
        a formatted data frame containing data of a specified state
    df_county : data frame object
        a formatted data frame containing data of a specified county
    county_index_num : int
        the index number of a specified county in the dataset
    state : str
        the name of the specified state
    county : str
        the name of the specified county
    days : date[]
        list of dates used from dataset
    start_data_date : str
        start date date represented as a string
    latest_data_date: str
        latest date of data represented as a string
    """

    df_state = 0
    df_county = 0
    county_index_num = 0
    state = ""
    county = ""
    days = []
    start_data_date = 0
    latest_data_date = 0

    def __init__(self, state):
        self.state = state
        self.get_dates_since_start()
        self.find_state()

    def find_state(self):
        """ Return the correct state data if it exists (Data frame object) """
        is_state = df_deaths['Province_State'] == self.state  # Assign true value to x state
        self.df_state = df_deaths[is_state]  # Filter all data of x state
        return self.df_state

    def get_state_name(self):
        """ Accessor for state (str) """
        return self.state

    def set_county(self, county):
        """ Mutator for county """
        self.county = county
        self.find_county()

    def find_county(self):
        """ Return the correct county data if it exists (Data frame object) """
        is_county = (df_deaths['Admin2'] == self.county) & (df_deaths['Province_State'] == self.state)  # Assign true value to x county
        self.df_county = df_deaths[is_county]  # Filter all data of x county
        self.county_index_num = self.df_county.loc[self.df_county['Admin2'] == self.county].index[0]  # Get index of correct county
        return self.df_county

    def get_county_name(self):
        """ Return name of a county (str) """
        return self.county

    def get_county_deaths_over_time(self):
        """ Return list of daily deaths for a county (int[]) """
        confirmed = []  # Create list of confirmed cases
        for i in range(len(self.get_days())):
            # add to confirmed list; formatted as [column][row]
            confirmed.append(self.df_county[self.days[i]][self.get_county_index()])
        return confirmed

    def get_county_index(self):
        """ Accessor for county_index_num (int) """
        return self.county_index_num

    def get_latest_data_date(self):
        """ Accessor for latest_data_date (date) """
        return self.latest_data_date

    def get_total_state_deaths(self):
        """ Return total number of deaths in a state (int) """
        filtered_df_confirmed = df_deaths[df_deaths['Province_State'] == self.state]
        new_df_confirmed = filtered_df_confirmed.groupby(['Admin2'])[self.get_latest_data_date()].sum().reset_index()
        new_df_confirmed = new_df_confirmed.sort_values(by=[self.get_latest_data_date()], ascending=[False]).reset_index()

        case_total = 0
        for i in range(len(new_df_confirmed)):
            case_total += new_df_confirmed[self.get_latest_data_date()][i]
        return case_total

    def get_total_state_deaths_over_time(self):
        """ Return daily totals of confirmed cases each day since start in a state (int[]) """
        filtered_df_confirmed = df_deaths[df_deaths['Province_State'] == self.get_state_name()]
        filtered_df_confirmed = filtered_df_confirmed.reset_index()  # Reset indices
        num_of_counties = filtered_df_confirmed.__len__()
        confirmed = []
        for date in range(len(self.get_days())):
            county_daily_total = 0
            for county in range(num_of_counties):
                county_daily_total += filtered_df_confirmed[self.get_days()[date]][county]
            confirmed.append(county_daily_total)
        return confirmed

    def get_all_counties(self):
        """ Return all counties in a state sorted by highest to lowest number of confirmed cases """
        filtered_df_confirmed = df_deaths[df_deaths['Province_State'] == self.state]
        new_df_confirmed = filtered_df_confirmed.groupby(['Admin2'])[self.get_latest_data_date()].sum().reset_index()
        new_df_confirmed = new_df_confirmed.sort_values(by=[self.get_latest_data_date()], ascending=[False]).reset_index()
        return new_df_confirmed['Admin2']

    def get_all_counties_total_deaths(self):
        """ Return all counties current number of cases sorted highest to lowest (data frame object) """
        print(self.get_latest_data_date())
        filtered_df_confirmed = df_deaths[df_deaths['Province_State'] == self.state]
        new_df_confirmed = filtered_df_confirmed.groupby(['Admin2'])[self.get_latest_data_date()].sum().reset_index()
        new_df_confirmed = new_df_confirmed.sort_values(by=[self.get_latest_data_date()], ascending=[False]).reset_index()
        return new_df_confirmed[self.get_latest_data_date()]

    def get_dates_since_start(self):
        """ Calculate which dates to use from datasets (date[]) """
        days = []
        start_data_date = date(2020, 3, 1)
        latest_data_date = date(2020, 4, 19)
        delta = timedelta(days=1)
        while start_data_date <= latest_data_date:
            days.append(start_data_date.strftime("%#m/%#d/%y"))  # Add dates to days list
            start_data_date += delta
        self.days = days
        self.start_data_date = date(2020, 3, 1).strftime("%#m/%#d/%y")
        self.latest_data_date = date(2020, 4, 19).strftime("%#m/%#d/%y")
        return days

    def get_days(self):
        """ Accessor for days (date[]) """
        return self.days

    def get_daily_state_deaths(self):
        """ Return daily change in confirmed cases in a specified state """
        daily_cases = []
        count = 0
        state_cases = self.get_total_state_deaths_over_time()  # Program runs faster when this is duplicated
        for i in state_cases:
            if count < state_cases.__len__() - 1:
                daily_cases.append(
                    state_cases[count+1] - state_cases[count])
                count += 1
        return daily_cases

    def get_daily_county_deaths(self):
        """ Return daily change in confirmed cases in a specified county """
        daily_cases = []
        count = 0
        county_cases = self.get_county_deaths_over_time()

        for i in county_cases:
            if count < county_cases.__len__() - 1:
                if county_cases[count+1] - county_cases[count] < 0:
                    daily_cases.append(0)
                else:
                    daily_cases.append(county_cases[count+1] - county_cases[count])
                count += 1
        return daily_cases


class States:
    """
    A class used to find information about states

    ...

    Attributes
    ----------
    df_usa : data frame
        data frame of entire states and counties dataset
    df_states : data frame
        a formatted data frame containing data of all 50 states
    softed_df : data frame
        a formatted data frame to group all counties with their associated state separated by commas
    counties : str[]
        list of counties formatted as strings
    state : str
        name of specified state
    state_index_codes : (dict of str: int)
        dictionary of all states and their associated index

    """
    df_usa = pd.read_csv('Datasets/states_and_counties.csv')

    df_states = df_usa['Province_State'].unique()
    sorted_df = df_usa.groupby(['Province_State'])['Admin2'].apply(", ".join)

    counties = []
    state = ""

    state_index_codes = {
        'Alabama': 0,
        'Alaska': 1,
        'Arizona': 2,
        'Arkansas': 3,
        'California': 4,
        'Colorado': 5,
        'Connecticut': 6,
        'Delaware': 7,
        'Florida': 8,
        'Georgia': 9,
        'Hawaii': 10,
        'Idaho': 11,
        'Illinois': 12,
        'Indiana': 13,
        'Iowa': 14,
        'Kansas': 15,
        'Kentucky': 16,
        'Louisiana': 17,
        'Maine': 18,
        'Maryland': 19,
        'Massachusetts': 20,
        'Michigan': 21,
        'Minnesota': 22,
        'Mississippi': 23,
        'Missouri': 24,
        'Montana': 25,
        'Nebraska': 26,
        'Nevada': 27,
        'New Hampshire': 28,
        'New Jersey': 29,
        'New Mexico': 30,
        'New York': 31,
        'North Carolina': 32,
        'North Dakota': 33,
        'Ohio': 34,
        'Oklahoma': 35,
        'Oregon': 36,
        'Pennsylvania': 37,
        'Rhode Island': 38,
        'South Carolina': 39,
        'South Dakota': 40,
        'Tennessee': 41,
        'Texas': 42,
        'Utah': 43,
        'Vermont': 44,
        'Virginia': 45,
        'Washington': 46,
        'West Virginia': 47,
        'Wisconsin': 48,
        'Wyoming': 49,
    }

    def set_state(self, state):
        """ Mutator for state """
        self.state = state
        self.find_counties_in_state()

    def get_state(self):
        """ Accessor for state """
        return self.state

    def get_state_index_code(self):
        """ Accessor for state_index_code """
        return self.state_index_codes[self.get_state()]

    def get_state_index_code_keys(self):
        """ Accessor for keys in state_index_codes """
        return self.state_index_codes.keys()

    def find_counties_in_state(self):
        """ Find all counties in each state and separate them into separate words and add to global counties list"""
        sorted_as_string = self.sorted_df[self.get_state_index_code()]
        counties = []
        word = ''
        count = 0
        for i in range(len(sorted_as_string)):
            if sorted_as_string[i] != ',':
                word += sorted_as_string[i]
            else:
                counties.append(word.strip())
                count += 1
                word = ''
        self.counties = counties

    def get_counties_in_state(self):
        """ Accessor for counties """
        return self.counties


class Country:
    """
    A class used to find information about the United States

    ...

    Attributes
    ----------
    df_usa : data frame
        data frame of entire states and counties dataset
    df_states : data frame
        a formatted data frame containing data of all 50 states

    state : str
        name of specified state

    """
    df_usa = pd.read_csv('Datasets/USA-04-18-2020.csv')

    df_states = df_usa['Province_State'].unique()

    def get_top_ten_confirmed_states(self):
        df = self.df_usa
        df = df.sort_values(by=['Confirmed'], ascending=[False]).head(10).reset_index()
        return df['Province_State']

    def get_top_ten_state_cases(self):
        df = self.df_usa
        df = df.sort_values(by=['Confirmed'], ascending=[False]).head(10).reset_index()
        return df['Confirmed']

    def get_top_ten_deaths_states(self):
        df = self.df_usa
        df = df.sort_values(by=['Deaths'], ascending=[False]).head(10).reset_index()
        return df['Province_State']

    def get_top_ten_state_deaths(self):
        df = self.df_usa
        df = df.sort_values(by=['Deaths'], ascending=[False]).head(10).reset_index()
        return df['Deaths']


