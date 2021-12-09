"""This module is responsible for dealing with the covid api requests and covid update scheduling"""

import sched
import time
import json
from uk_covid19 import Cov19API

with open("covid_dashboard_config.json", "r") as config_file:
    data = json.load(config_file)

covid_scheduler = sched.scheduler(time.time, time.sleep)

local_covid_data = []
national_covid_data = []

def parse_csv_data(csv_filename:str)->list:
    """
        Functionality:
        ---------------
            Takes a csv file and puts the data in a list of strings 
            so that they can be processed later

        Parameters:
        ---------------
            csv_filename : str
                The name of the file to be open and read from

        Returns:
        ---------------
            data: list
                The resulting list of strings
    """
    with open(csv_filename, "r") as csv_file:
        lines = csv_file.readlines()
        data = []
        for line in lines:
            data.append(line[:-1])
        return data

def process_covid_csv_data(covid_csv_data:list)->tuple:
    """
        Functionality:
        ---------------
            Takes a list of strings (intended to be the result from the 
            fuction parse_csv_data) and calculates and returns
            the the number of new cases in the last 7 days, the current 
            number of people in hospital and the total cumulative
            number of deaths

        Parameters:
        ---------------
            covid_csv_data: list
                A list of strings (as produced by the function parse_csv_data)

        Returns:
        ---------------
            last_7_day_cases: int
                The number of new cases in the past 7 days

            current_hospital_cases: int
                The number of people currently in hospital due to covid

            total_deaths: int
                The total number of cumulative deaths from covid
    """
    last_7_day_cases = 0
    current_hospital_cases = int(covid_csv_data[1].split(",")[5])
    total_deaths = int(covid_csv_data[14].split(",")[4])
    for i in range(3, 10):#may need swapping to (2, 9) depending on whether correct on spec or not
        last_7_day_cases += int(covid_csv_data[i].split(",")[6])
    return last_7_day_cases, current_hospital_cases, total_deaths

def covid_API_request(location:str="Exeter", location_type:str="ltla")->dict:
    """
        Functionality:
        ---------------
            Used to query the covid19 api and to return results for the relevant area

        Parameters:
        ---------------
            location: str
                The location for which the user wishes to find covid data for.
                This is automatically set to Exeter

            location_type: str
                The sort of location that the user is looking for (is it a county, a country, etc)

        Returns:
        ---------------
            api.get_json(): dict
                Returns a dictionary with the covid api data 
    """
    filters = ["areaType="+location_type,"areaName="+location]
    data_required = {
    "areaCode": "areaCode",
    "areaName": "areaName",
    "areaType": "areaType",
    "date": "date",
    "cumDailyNsoDeathsByDeathDate": "cumDailyNsoDeathsByDeathDate",
    "hospitalCases": "hospitalCases",
    "newCasesBySpecimenDate": "newCasesBySpecimenDate"
    }
    
    api = Cov19API(filters=filters, structure=data_required)
    try:
        return api.get_json()
    except:
        return None

def process_api_data(location:str="Exter", location_type:str="ltla")->None:
    """
        Functionality:
        ---------------
            Calls the funtion covid_API_request and then processes the api data to
            product the data to be displayed on the dashboard

        Parameters:
        ---------------
            location: str
                The location for which the user wishes to find covid data for. 
                This is automatically set to Exeter

            location_type: str
                The sort of location that the user is looking for (is it a county, a country, etc)

        Returns:
        ---------------
            last_7_day_cases: int
                The number of new cases in the past 7 days

            current_hospital_cases: int
                The number of people currently in hospital due to covid

            total_deaths: int
                The total number of cumulative deaths from covid
    """
    global local_covid_data
    global national_covid_data
    covid_data_request = covid_API_request(location, location_type)
    if covid_data_request != None:
        covid_data = covid_data_request["data"]
        #finding number of cases in last 7 days
        last_7_day_cases = 0
        counter = 0
        items_added = 0
        while True:
            try:
                last_7_day_cases += int(covid_data[counter]["newCasesBySpecimenDate"])
                items_added += 1
            except TypeError:
                pass
            finally:
                counter+=1
                if items_added == 7:
                    break

        #finding hospital cases
        if covid_data[0]["areaType"]!="nation":
            current_hospital_cases = "There is no data for this type of location"
        else:
            counter = 0
            while type(covid_data[counter]["hospitalCases"]) != int:
                counter+=1
            current_hospital_cases = covid_data[counter]["hospitalCases"]

        #finding total deaths
        counter = 0
        if covid_data[0]["areaType"]!="nation":
            total_deaths = "There is no data for this type of location"
        else:
            while covid_data[counter]["cumDailyNsoDeathsByDeathDate"] is None:
                counter+=1
            total_deaths = covid_data[counter]["cumDailyNsoDeathsByDeathDate"]

        #updating correct data structure
        if location_type=="ltla":
            local_covid_data = [last_7_day_cases, current_hospital_cases, total_deaths]
        elif location_type=="nation":
            national_covid_data = [last_7_day_cases, current_hospital_cases, total_deaths]
    
    else:
        #updating correct data structure
        if location_type=="ltla":
            local_covid_data = ["-","-","-"]
        elif location_type=="nation":
            national_covid_data = ["-","-","-"]
    return None

def schedule_covid_updates(update_interval:int, update_name:str)->dict:
    """
        Functionality:
        ---------------
            Schedules a new covid data update for both the local and national data

        Parameters:
        ---------------
            update_interval: int
                The time until the scheduler should update the covid data
    
            update_name: str
                The name of the update that has caused the scheduling of the covid data update

        Returns:
        ---------------
            a key-value pair: dict
                Returns a dictionary with the key being the update name and the value being a list containing
                both the local and national scheduler objects
    """
    return({update_name:[covid_scheduler.enter(update_interval, 1, process_api_data, (data["local_location"], "ltla")), covid_scheduler.enter(update_interval, 1, process_api_data, (data["national_location"], "nation"))]})

def return_covid_data(location_type:str)->list:
    """
        Functionality:
        ---------------
            Returns the local or national covid data depending on the input

        Parameters:
        ---------------
            location_type: str
                Which sort of data should be returned (local/nation)

        Returns:
        ---------------
            local_covid_data: list
                A list with the local covid data

            national_covid_data: list
                A list with the national covid data
    """
    if location_type == "local":
        return local_covid_data
    elif location_type == "nation":
        return national_covid_data
