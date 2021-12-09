"""This module tests the covid_data_handler module"""

from covid_data_handler import parse_csv_data
from covid_data_handler import process_covid_csv_data
from covid_data_handler import covid_API_request
from covid_data_handler import process_api_data
from covid_data_handler import schedule_covid_updates
from covid_data_handler import return_covid_data

def test_parse_csv_data():
    """
        Tests the parse csv data function
    """
    data = parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 639,  "Expected a different data length"

def test_process_covid_csv_data():
    """
        Tests the process covid csv function
    """
    last7days_cases , current_hospital_cases , total_deaths = \
        process_covid_csv_data ( parse_csv_data ('nation_2021-10-28.csv' ) )
    assert last7days_cases == 240_299, "Expected different last 7 days cases"
    assert current_hospital_cases == 7_019, "Expected different current hospital cases"
    assert total_deaths == 141_544, "Expected different total deaths"

def test_covid_API_request():
    """
        Tests the covid api request function
    """
    default_data = covid_API_request()
    local_data = covid_API_request("Exeter", "ltla")
    national_data = covid_API_request("England", "nation")
    assert default_data == local_data, "Expected local and default to be the same"
    assert local_data != national_data, "Expected local and national to be different"
    assert isinstance(default_data, dict), "Expected default data to be dict"
    assert isinstance(local_data, dict), "Expected local data to be dict"
    assert isinstance(national_data, dict), "Expected national data to be dict"

def test_process_api_data():
    """
        Tests the procces covid api function
    """
    process_api_data("Exeter", "ltla" ), "Process api data is broken"

def test_schedule_covid_updates(): 
    """
        Tests the schedule covid update function
    """ 
    data = schedule_covid_updates(update_interval=10, update_name='update test')
    assert (isinstance(data, dict) and len(data)==1), "Wrong type returned"
    assert list(data.keys())[0] == "update test", "Expected different dictionary key"
    assert len(list(data.values())[0]) == 2, "Expected length of the dictionary to be 2"

def test_return_covid_data():
    """
        Tests the return covid data function
    """
    local_data = return_covid_data("local")
    national_data = return_covid_data("local")
    none_data = return_covid_data("")
    assert isinstance(local_data, list), "Expected list"
    assert isinstance(national_data, list), "Expected list"
    assert none_data == None, "Expected None"