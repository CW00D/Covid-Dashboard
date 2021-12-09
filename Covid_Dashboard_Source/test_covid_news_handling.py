"""This module tests the covid_news_handling module"""

from covid_news_handling import news_API_request
from covid_news_handling import update_news
from covid_news_handling import schedule_news_updates
from covid_news_handling import return_news_data

def test_news_API_request():
    """
        Tests the news api request function
    """
    assert news_API_request(), "News api request is broken"
    assert news_API_request('Covid COVID-19 coronavirus') == news_API_request(), "Default and given terms results arent the same"
    assert isinstance(news_API_request(), list), "Expected a list"

def test_update_news():
    """
        Tests the update news function
    """
    update_news('test'), "Update news is broken"

def test_schedule_news_updates():
    """
        Tests the schedule news update function
    """ 
    data = schedule_news_updates(update_interval=10, update_name='update test')
    assert (isinstance(data, dict) and len(data)==1), "Wrong type returned"
    assert list(data.keys())[0] == "update test", "Expected different dictionary key"

def test_return_news_data():
    """
        Tests the return news data function
    """
    news_data = return_news_data()
    assert isinstance(news_data, list), "Expected list"
