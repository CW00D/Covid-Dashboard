# __Covid Dashboard__

## Introduction
This package generates a covid dashboard that displays covid data for the user according to the users requirements as entered in the config file.

**Author:** Christian Wood  
**License:** MIT  
**Date:** 2021  
**Version:** 1.0.0  
**Github:**  https://github.com/CW00D/Covid-Dashboard

## Prerequisites
In order for the covid_dashboard to work, you must ensure that none of the files within the covid_dashboard folder are deleted. There are also some requirements for the modules and languages that you must have installed on your machine.
	
They are outlined below:
- sched
- time
- json
- uk_covid19
- requests
- flask
- logging
- python 3

In addition, you will require your own new_api key which you can find on https://newsapi.org/. You should then enter the key you are given into the config file as outlined in the configuration instructions.

## Installation Instructions:
Simply install the package and you are good to go

## Configuration Instructions:
There is a file called covid_dashboard_config.json which contains the configuration data for the covid dashboard. From there you will be able to change the locations for which the dashboard displays data and the search terms and language for the search results that the dashboard should display.  

**You should also change the value of the api_key to whatever your news api key is. You should replace \<Enter Your API Key Here> with said api key.**

## Operation Instructions:
#### How to open:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;You must first ensure that the code is running and must then open a browser and navigate to http://127.0.0.1:5000/index

### The dashboard is split into three sections:
1. Middle Section:{"title":update_to_create["update_name"], "content":content, "repeat":(update_to_create["update_repeat"]), "covid_update":(update_to_create["covid_update"]), "news_update":(update_to_create["news_update"])}
The middle section contains the covid information collected from the api about the area according to the config file. Below it is the updates area where you can create a new update. From here you will be able to specify whether you want the update to be a covid or news udpate (note can be both but not neither). You must specify a time for the update to happen and whether or not the update should repeat every day at the same time. The updates name must be unique and not be in the updates currently scheduled. The update name should also not contain any spaces (recomendation:use underscores as a replacement).

2. Left Section:
The left section contains the updates that you have created. Each box contains the update information. You are able to cancel an update simply by clicking the close button at the top right of the box containing the update you wish to close.
        
3. Right Section:
The right section contains the news articles that contain any of the keywords as specified in the config file. By clicking the hyperlick at the bottom of each box, you will be able to open the relevant news article. Similarly to the updates, you will be able to close news articles to remove them from your dashboard so as to load new news articles. You do this by clicking the close button at the top right of the box containing the news article to be remove.

### Ensure:
As the user you should ensure that the wifi is on as otherwise the dashboard will not have any data to display.

## Developer Documentation:
The developer documentation can be found within the folder docs/build/html. You should then open the index.html file.

## Testing:
The code will automatically run a series of tests before executing the code.

## File Manifest:
- .pytest_cache - a folder containing data from the pytest's cache plugin
- Covid_Dashboard_Source
    - \_\_pycache\_\_ - contains docstrings
    - static with a sub folder images
        - covid.png
        - favicon.ico
    - templates
        - index.html
    - covid_dashboard_displayer.py
    - covid_data_handler.py
    - covid_news_handling.py
    - test_covid_dashboard_displayer.py
    - test_covid_data_handler.py
    - test_covid_news_handling.py
- docs
    - build
        - doctrees - contains the doctrees used in the generation of the html pages
        - html - contains the html files for the documentation
    - source - contains all the rst files to make html pages
    - make.bat
    - Makefile
- covid_dashboard_config.json
- covid_dashboard.log
- LICENSE.txt
- nation_2021-10-28.csv
- README.md
- setup.py
