"""This module will open the covid dashboard and deal with the user"""

import urllib
import logging
import json
import pytest
import time
from flask import Flask, render_template, request, redirect
from covid_data_handler import process_api_data, schedule_covid_updates, return_covid_data, covid_scheduler
from covid_news_handling import schedule_news_updates, update_news, return_news_data, news_scheduler

logging.basicConfig(filename='covid_dashboard.log', level=logging.INFO)

with open("covid_dashboard_config.json", "r") as config_file:
    data = json.load(config_file)

app = Flask(__name__)

process_api_data(data["local_location"], "ltla")
process_api_data(data["national_location"], "nation")
update_news()

updates = []
covid_updates = {}
news_updates = {}

closed_news_articles = []
closed_updates = []

def caluclate_time_for_update(update_time:str)->int:
    """
        Functionality:
        ---------------
            Takes the time at which the update should be executed and finds the number of
            seconds until the update should happen.

        Parameters:
        ---------------
            update_time : str
                The value inputed by the user for which the update should happen

        Returns:
        ---------------
            time_till_update: int
                The number of seconds until the update should be executed
    """
    time_of_update_in_seconds = int(update_time.split(":")[0])*3600 + int(update_time.split(":")[1])*60
    current_time = time.strftime("%H:%M:%S").split(":")
    time_now = int(current_time[0])*3600 + int(current_time[1])*60 + int(current_time[2])
    time_till_update = time_of_update_in_seconds - time_now
    if time_till_update < 0:
        time_till_update += 86400
    return time_till_update

def create_new_update(update_to_create:dict)->None:
    """
        Functionality:
        ---------------
            Creates a new update when called

        Parameters:
        ---------------
            update_to_create : dict
                A dictionary containing the data to create an update

        Returns:
        ---------------
            None
    """
    already_in_updates = False
    for update in updates:
        if update_to_create["update_name"] == update["title"]:
            logging.warning("Update name already in use")
            already_in_updates = True
    if not already_in_updates:
        if update_to_create["covid_update"] or update_to_create["news_update"]:
            content = "Covid Update: "+ str(update_to_create["covid_update"]) + " | News Update: " + str(update_to_create["news_update"]) + " | Update Time: " + update_to_create["update_time"] + " | Repeat: " + str(update_to_create["update_repeat"])
            new_update = {"title":update_to_create["update_name"], "content":content, "repeat":(update_to_create["update_repeat"]), "covid_update":(update_to_create["covid_update"]), "news_update":(update_to_create["news_update"])}
            updates.append(new_update)
            time_for_update= caluclate_time_for_update(update_to_create["update_time"])
            if update_to_create["covid_update"]:
                logging.info("Creating covid update")
                covid_updates.update(schedule_covid_updates(time_for_update, update_to_create["update_name"]))
            if update_to_create["news_update"]:
                logging.info("Creating news update")
                news_updates.update(schedule_news_updates(time_for_update, update_to_create["update_name"]))
        else:
            logging.warning("Not covid or news update")

def remove_updates(update:dict)->None:
    """
        Functionality:
        ---------------
            Used to remove and cancel updates from the covid and news update lists and schedulers

        Parameters:
        ---------------
            update : dict
                A dictionary containg the update to remove

        Returns:
        ---------------
            None
    """
    if update["title"] in covid_updates:
        if covid_updates[update["title"]][0] in covid_scheduler.queue and covid_updates[update["title"]][1] in covid_scheduler.queue:
            logging.info("Cancelling covid update")
            covid_scheduler.cancel(covid_updates[update["title"]][0])
            covid_scheduler.cancel(covid_updates[update["title"]][1])
        if update["title"] in news_updates:
            if news_updates[update["title"]] in news_scheduler.queue:
                logging.info("Cancelling news update")
                news_scheduler.cancel(news_updates[update["title"]])
        updates.remove(update)

def restore_state()->None:
    """
        Functionality:
        ---------------
            Used to read the log file and reload the previous state accordingly

        Parameters:
        ---------------
            None

        Returns:
        ---------------
            None
    """
    with open('covid_dashboard.log') as logfile:
        for line in logfile.readlines():
            if line[:4] == 'INFO':
                if line.split("=")[0][-10:] == "alarm_item":
                    logging.info("Getting data for update to reremove")
                    update_to_remove = line.split("=")[1].split(" ")[0]
                    if update_to_remove != "There+are+currently+no+updates+to+display":
                        for update in updates:
                            if update["title"] == update_to_remove:
                                break
                        remove_updates(update)

                elif line.split("=")[0][-5:] == "alarm":
                    logging.info("Getting data to recreate an update")
                    update_values_to_add = {"update_name":"", "update_time":"", "update_repeat":False, "covid_update":False, "news_update":False}
                    args = line.split('&')
                    args[-1] = args[-1].split(" ")[0]
                    update_values_to_add["update_time"]=args[0][-7:-5]+":"+args[0][-2:]
                    update_values_to_add["update_name"]=args[1][4:]
                    if len(args)>= 3:
                        type_of_value_to_add = args[2].split("=")[0]
                        value_to_add = args[2].split("=")[1]
                        if type_of_value_to_add == "repeat" and value_to_add=="repeat":
                            update_values_to_add["repeat"]=True
                        elif type_of_value_to_add == "covid-data" and value_to_add=="covid-data":
                            update_values_to_add["covid_update"]=True
                        elif type_of_value_to_add == "news" and value_to_add=="news":
                            update_values_to_add["news_update"]=True
                    if len(args)>= 4:
                        type_of_value_to_add = args[3].split("=")[0]
                        value_to_add = args[3].split("=")[1]
                        if type_of_value_to_add == "repeat" and value_to_add=="repeat":
                            update_values_to_add["repeat"]=True
                        elif type_of_value_to_add == "covid-data" and value_to_add=="covid-data":
                            update_values_to_add["covid_update"]=True
                        elif type_of_value_to_add == "news" and value_to_add=="news":
                            update_values_to_add["news_update"]=True
                    if len(args)>= 5:
                        type_of_value_to_add = args[4].split("=")[0]
                        value_to_add = args[4].split("=")[1]
                        if type_of_value_to_add == "repeat" and value_to_add=="repeat":
                            update_values_to_add["repeat"]=True
                        elif type_of_value_to_add == "covid-data" and value_to_add=="covid-data":
                            update_values_to_add["covid_update"]=True
                        elif type_of_value_to_add == "news" and value_to_add=="news":
                            update_values_to_add["news_update"]=True
                    create_new_update(update_values_to_add)

                elif line.split("=")[0][-5:] == "notif":
                    news_article_title = line.split("=")[1].split(" ")[0]
                    if news_article_title == "There+are+currently+no+new+news+articles+to+display":
                        pass
                    else:
                        logging.info("Adding a previously closed news article to closed articles")
                        closed_news_articles.append(news_article_title)

pytest.main()
restore_state()

@app.route("/")
def return_to_dashboard():
    """
        Functionality:
        ---------------
            Redirects to /index

        Parameters:
        ---------------
            None

        Returns:
        ---------------
            redirect : function
            Redirects to /index
    """
    return redirect("/index")

@app.route("/index")
def covid_dashboard():
    """
        Functionality:
        ---------------
            Deals with data inputs from the website and displays the html with relevan data

        Parameters:
        ---------------
            None

        Returns:
        ---------------
            render_template : function
                html file with relevant data
    """
#Possible responses from dashboard
    covid_update = request.args.get("covid-data")=="covid-data"
    news_update = request.args.get("news")=="news"
    update_closed = request.args.get("alarm_item")
    news_closed = request.args.get("notif")
    update_time = request.args.get("alarm")
    update_label = request.args.get("two")
    update_repeat = request.args.get("repeat")=="repeat"

#Getting the data to display
    local_covid_data = return_covid_data("local")
    national_covid_data = return_covid_data("nation")
    news_data = return_news_data()

#Removing news articles
    if news_closed:
        logging.info("Adding news article to closed articles")
        closed_news_articles.append(urllib.parse.quote_plus(news_closed))
    for article in news_data:
        if urllib.parse.quote_plus(article["title"]) in closed_news_articles:
            logging.info("Removing news article")
            news_data.remove(article)

#Adding an update to closed updates
    if update_closed:
        logging.debug("Adding update to closed updates before finished")
        closed_updates.append(update_closed)

#Removing closed updates
    for update in updates:
        if update["title"] in closed_updates:
            logging.info("Update closed")
            remove_updates(update)
            closed_updates.remove(update["title"])

        else:
            if update["title"] in covid_updates:
                if covid_updates[update["title"]][0] not in covid_scheduler.queue and covid_updates[update["title"]][1] not in covid_scheduler.queue and update["covid_update"]:
                    if update["repeat"]:
                        logging.info("Repeating covid update")
                        del covid_updates[update["title"]]
                        covid_updates.update(schedule_covid_updates(86400, update["title"]))
                    else:
                        logging.info("Adding covid update to closed updates after finished")
                        closed_updates.append(update["title"])
            if update["title"] in news_updates:
                if news_updates[update["title"]] not in news_scheduler.queue and update["news_update"]:
                    if update["repeat"]:
                        logging.info("Repeating news update")
                        del news_updates[update["title"]]
                        news_updates.update(schedule_news_updates(86400, update["title"]))
                    elif update["title"] not in closed_updates:
                        logging.info("Adding news update to closed updates after finished")
                        closed_updates.append(update["title"])

#Adding a new update
    if update_label:
        if update_time != "":
            if len(update_label.split(" "))==1:
                logging.info("New update created")
                update_to_create = {"update_name":update_label, "update_time":update_time,
                "update_repeat":update_repeat, "covid_update":covid_update, "news_update":news_update}
                create_new_update(update_to_create)
            else:
                logging.warning("Update name contains spaces")
        else:
            logging.warning("Time for update not set")

#Running both schedulers
    covid_scheduler.run(blocking=False)
    news_scheduler.run(blocking=False)

#Setting data for toasts
    news_to_display = news_data[0:5]
    if len(news_to_display) == 0:
        logging.info("No more news articles available")
        news_to_display = [{"title":"There are currently no new news articles to display", "content":"No content", "url":""}]

    updates_to_display = updates
    if len(updates_to_display) == 0:
        logging.info("No updates available")
        updates_to_display = [{"title":"There are currently no updates to display", "content":"No content"}]

#Returning template
    return render_template("index.html", favicon="favicon.ico", image="covid.png",
    title="Personal Covid Dashboard", location=data["local_location"],
    local_7day_infections = local_covid_data[0], nation_location=data["national_location"],
    national_7day_infections=national_covid_data[0], hospital_cases=national_covid_data[1],
    deaths_total=national_covid_data[2], news_articles=news_to_display, updates=updates_to_display)

if __name__ == "__main__":
    app.run()
