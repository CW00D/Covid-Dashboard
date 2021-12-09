"""This module is responsible for dealing with the news api requests and news update scheduling"""

import sched
import time
import json
import requests

with open("covid_dashboard_config.json", "r") as config_file:
    data = json.load(config_file)

news_scheduler = sched.scheduler(time.time, time.sleep)

news_data = []

def news_API_request(covid_terms:str="Covid COVID-19 coronavirus")->list:
    """
        Functionality:
        ---------------
            Used to return all the news articles from the news api with the given keywords

        Parameters:
        ---------------
            covid_terms: string
                The keywords used to search the news api

        Returns:
        ---------------
            news_articles: list
                The news articles from the news api with the given keywords
    """
    news_articles = []
    for keyword in covid_terms.split(" "):
        url = ("https://newsapi.org/v2/top-headlines?q="+keyword+"&language="+
        data["search_result_language"]+"&apiKey="+data["api_key"])
        try:
            response = requests.get(url)
        except:
            return [{'title': "There are currently no new news articles to display", "url": "http://127.0.0.1:5000/", "content":"You have no wifi"}]
        news_articles += response.json()["articles"]
    return news_articles

def update_news(covid_terms:str=data["search terms"])->None:
    """
        Functionality:
        ---------------
            Used to update the news_data structure with the new news

        Parameters:
        ---------------
            covid_terms: string
                The keywords used to search the news api

        Returns:
        ---------------
            None
    """
    global news_data
    news_data = news_API_request(covid_terms)
    return None

def schedule_news_updates(update_interval:int, update_name:str)->dict:
    """
        Functionality:
        ---------------
            Schedules a new news data update

        Parameters:
        ---------------
            update_interval: int
                The time until the scheduler should update the news data

            update_name: str
                The name of the update that has caused the scheduling of the news data update

        Returns:
        ---------------
            a key-value pair: dict
                Returns a dictionary with the key being the update name and the 
                value being news scheduler object
    """
    return({update_name:news_scheduler.enter(update_interval, 1, update_news, ())})

def return_news_data()->list:
    """
        Functionality:
        ---------------
            Returns the news data

        Parameters:
        ---------------
            No parameters

        Returns:
        ---------------
            news_data: list
                A list with the news data
    """
    return news_data

news_API_request()