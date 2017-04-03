#!/home/kyle/anaconda3/bin/python3
import os
import schedule
import time
import bs4 as BeautifulSoup
import numpy as np
import pandas as pd
from random import randint
from selenium import webdriver
from collections import OrderedDict
from datetime import date
from datetime import datetime

os.chdir("/home/kyle/Dropbox/research/studyrooms")

powell_rooms = "http://calendar.library.ucla.edu/booking/powellstudy"
yrl_rooms = "http://calendar.library.ucla.edu/booking/rescommons"
yrl_pods = "http://calendar.library.ucla.edu/booking/pods"
driver = webdriver.PhantomJS("/home/kyle/programs/phantomjs/bin/phantomjs")
time.sleep(1)
scrape_time = str(datetime.now())[:-7]

def load_page(webpage):
    "This loads the given webpage in the webdriver"
    print("Loading page...")
    driver.get(webpage)
    time.sleep(randint(2,4))

def load_tomorrow():
    "This loads the page for tomorrow"
    today = date.today().timetuple()
    tomorrow = str(today.tm_mday + 1)
    driver.find_element_by_link_text(str(tomorrow)).click()
    time.sleep(randint(2,4))
    return

def load_secondday():
    "This loads the page for the day after tomorrow"
    today = date.today().timetuple()
    dayaftertom = str(today.tm_mday + 2)
    driver.find_element_by_link_text(str(dayaftertom)).click()
    page_source = driver.page_source
    time.sleep(randint(2,4))
    return


# Powell Rooms
load_page(powell_rooms)
powell_today = driver.page_source
load_tomorrow()
powell_tomorrow = driver.page_source
load_secondday()
powell_secondday = driver.page_source

soup_powell_0 = BeautifulSoup.BeautifulSoup(powell_today, "html.parser")
soup_powell_1 = BeautifulSoup.BeautifulSoup(powell_tomorrow, "html.parser")
soup_powell_2 = BeautifulSoup.BeautifulSoup(powell_secondday, "html.parser")

rooms_powell_0 = soup_powell_0.find_all("a", class_="lc_rm_a")
rooms_powell_1 = soup_powell_1.find_all("a", class_="lc_rm_a")
rooms_powell_2 = soup_powell_2.find_all("a", class_="lc_rm_a")

open_powell_0 = []
for x in rooms_powell_0:
    open_powell_0.append(str(x))

open_powell_1 = []
for x in rooms_powell_1:
    open_powell_1.append(str(x))

open_powell_2 = []
for x in rooms_powell_2:
    open_powell_2.append(str(x))

df_powell_0 = pd.DataFrame(open_powell_0, columns=["text"])
df_powell_0 = df_powell_0["text"].str.split(",", expand = True)
df_powell_0["current_time"] = scrape_time
df_powell_0

df_powell_1 = pd.DataFrame(open_powell_1, columns=["text"])
df_powell_1 = df_powell_1["text"].str.split(",", expand = True)
df_powell_1["current_time"] = scrape_time
df_powell_1

df_powell_2 = pd.DataFrame(open_powell_2, columns=["text"])
df_powell_2 = df_powell_2["text"].str.split(",", expand = True)
df_powell_2["current_time"] = scrape_time
df_powell_2

df_powell_0.to_csv("/home/kyle/Dropbox/research/studyrooms/data/" + "powell_0_" + scrape_time + ".csv", index=False)
df_powell_1.to_csv("/home/kyle/Dropbox/research/studyrooms/data/" + "powell_1_" + scrape_time + ".csv", index=False)
df_powell_2.to_csv("/home/kyle/Dropbox/research/studyrooms/data/" + "powell_2_" + scrape_time + ".csv", index=False)


# YRL Rooms
load_page(yrl_rooms)
yrl_room_today = driver.page_source
load_tomorrow()
yrl_room_tomorrow = driver.page_source
load_secondday()
yrl_room_secondday = driver.page_source

soup_yrl_room_0 = BeautifulSoup.BeautifulSoup(yrl_room_today, "html.parser")
soup_yrl_room_1 = BeautifulSoup.BeautifulSoup(yrl_room_tomorrow, "html.parser")
soup_yrl_room_2 = BeautifulSoup.BeautifulSoup(yrl_room_secondday, "html.parser")

rooms_yrl_room_0 = soup_yrl_room_0.find_all("a", class_="lc_rm_a")
rooms_yrl_room_1 = soup_yrl_room_1.find_all("a", class_="lc_rm_a")
rooms_yrl_room_2 = soup_yrl_room_2.find_all("a", class_="lc_rm_a")

open_yrl_room_0 = []
for x in rooms_yrl_room_0:
    open_yrl_room_0.append(str(x))

open_yrl_room_1 = []
for x in rooms_yrl_room_1:
    open_yrl_room_1.append(str(x))

open_yrl_room_2 = []
for x in rooms_yrl_room_2:
    open_yrl_room_2.append(str(x))

df_yrl_room_0 = pd.DataFrame(open_yrl_room_0, columns=["text"])
df_yrl_room_0 = df_yrl_room_0["text"].str.split(",", expand = True)
df_yrl_room_0["current_time"] = scrape_time
df_yrl_room_0

df_yrl_room_1 = pd.DataFrame(open_yrl_room_1, columns=["text"])
df_yrl_room_1 = df_yrl_room_1["text"].str.split(",", expand = True)
df_yrl_room_1["current_time"] = scrape_time
df_yrl_room_1

df_yrl_room_2 = pd.DataFrame(open_yrl_room_2, columns=["text"])
df_yrl_room_2 = df_yrl_room_2["text"].str.split(",", expand = True)
df_yrl_room_2["current_time"] = scrape_time
df_yrl_room_2

df_yrl_room_0.to_csv("/home/kyle/Dropbox/research/studyrooms/data/" + "yrl_room_0_" + scrape_time + ".csv", index=False)
df_yrl_room_1.to_csv("/home/kyle/Dropbox/research/studyrooms/data/" + "yrl_room_1_" + scrape_time + ".csv", index=False)
df_yrl_room_2.to_csv("/home/kyle/Dropbox/research/studyrooms/data/" + "yrl_room_2_" + scrape_time + ".csv", index=False)


# YRL pods
load_page(yrl_pods)
yrl_pod_today = driver.page_source
load_tomorrow()
yrl_pod_tomorrow = driver.page_source
load_secondday()
yrl_pod_secondday = driver.page_source

soup_yrl_pod_0 = BeautifulSoup.BeautifulSoup(yrl_pod_today, "html.parser")
soup_yrl_pod_1 = BeautifulSoup.BeautifulSoup(yrl_pod_tomorrow, "html.parser")
soup_yrl_pod_2 = BeautifulSoup.BeautifulSoup(yrl_pod_secondday, "html.parser")

rooms_yrl_pod_0 = soup_yrl_pod_0.find_all("a", class_="lc_rm_a")
rooms_yrl_pod_1 = soup_yrl_pod_1.find_all("a", class_="lc_rm_a")
rooms_yrl_pod_2 = soup_yrl_pod_2.find_all("a", class_="lc_rm_a")

open_yrl_pod_0 = []
for x in rooms_yrl_pod_0:
    open_yrl_pod_0.append(str(x))

open_yrl_pod_1 = []
for x in rooms_yrl_pod_1:
    open_yrl_pod_1.append(str(x))

open_yrl_pod_2 = []
for x in rooms_yrl_pod_2:
    open_yrl_pod_2.append(str(x))

df_yrl_pod_0 = pd.DataFrame(open_yrl_pod_0, columns=["text"])
df_yrl_pod_0 = df_yrl_pod_0["text"].str.split(",", expand = True)
df_yrl_pod_0["current_time"] = scrape_time
df_yrl_pod_0

df_yrl_pod_1 = pd.DataFrame(open_yrl_pod_1, columns=["text"])
df_yrl_pod_1 = df_yrl_pod_1["text"].str.split(",", expand = True)
df_yrl_pod_1["current_time"] = scrape_time
df_yrl_pod_1

df_yrl_pod_2 = pd.DataFrame(open_yrl_pod_2, columns=["text"])
df_yrl_pod_2 = df_yrl_pod_2["text"].str.split(",", expand = True)
df_yrl_pod_2["current_time"] = scrape_time
df_yrl_pod_2

df_yrl_pod_0.to_csv("/home/kyle/Dropbox/research/studyrooms/data/" + "yrl_pod_0_" + scrape_time + ".csv", index=False)
df_yrl_pod_1.to_csv("/home/kyle/Dropbox/research/studyrooms/data/" + "yrl_pod_1_" + scrape_time + ".csv", index=False)
df_yrl_pod_2.to_csv("/home/kyle/Dropbox/research/studyrooms/data/" + "yrl_pod_2_" + scrape_time + ".csv", index=False)

driver.quit()
