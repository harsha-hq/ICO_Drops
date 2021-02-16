# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 23:11:58 2021

@author: hvvel
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from datetime import date 
from urllib.parse import urljoin
import requests
import time
import datetime
import pandas as pd
import selenium.webdriver


today = date.today()
today = today.strftime("%Y/%m/%d")

ACTIVE_HEADER = ['Project','Project_Link', 'INTEREST', 'CATEGORY', 'END_TIME','COLLECTED_DATE']
UPCOMING_HEADER = ['Project','Project_Link', 'INTEREST', 'CATEGORY', 'START_DATE', 'COLLECTED_DATE']
ENDED_HEADER = ['Project','Project_Link', 'INTEREST', 'CATEGORY', 'END_DATE', 'MARKET_TICKER','COLLECTED_DATE']

ACTIVE_HEADER_LINK_DF = pd.DataFrame(columns=ACTIVE_HEADER)
UPCOMING_HEADER_LINK_DF = pd.DataFrame(columns=UPCOMING_HEADER)
ENDED_HEADER_LINK_DF = pd.DataFrame(columns=ENDED_HEADER)

active_link_var = 'https://icodrops.com/category/active-ico/'

upcoming_link_var = 'https://icodrops.com/category/upcoming-ico/'

ended_link_var = 'https://icodrops.com/category/ended-ico/'

active_RESPONSE = requests.get('https://icodrops.com/category/active-ico/')
active_SOUP = BeautifulSoup(active_RESPONSE.text, 'html.parser')
all_tab = active_SOUP.find(class_='col-lg-6 col-md-12 col-12 all')
active_POSTS = all_tab.find_all(class_='col-md-12 col-12 a_ico')
for post in active_POSTS:
    #print(post)
    name = post.find('div',class_='ico-main-info')
    if name is not None:
        project_name = name.find('a')
        project_name = project_name.get_text()
        print(project_name)
        project_link = name.find('a')['href']
        #print(project_link)
    active_interest = post.find('div',class_='interest')
    if active_interest is not None:
        interest = active_interest.get_text().replace('\n', '').replace("\t","")
        #print(interest)
    active_category = post.find('div',class_='ico-category-name')
    if active_category is not None:
        category = active_category.get_text().replace('\n', '').replace("\t","")
        #print(category)
    active_end_date = post.find('div',class_='date active')
    if active_end_date is not None:
        end_time = active_end_date.get_text().replace('\n', '').replace("\t","")
        print(end_time)
    ACTIVE_HEADER_LINK_DF = ACTIVE_HEADER_LINK_DF.append({'Project' : project_name,
                                    'Project_Link':project_link,
                                    'INTEREST': interest,
                                    'CATEGORY': category,
                                    'END_TIME': end_time,
                                    'COLLECTED_DATE' : today
                                    }, ignore_index=True)
ACTIVE_HEADER_LINK_DF.to_csv("ico_drops_active_projects.csv", index=False,encoding='utf-8-sig')


upcoming_RESPONSE = requests.get('https://icodrops.com/category/upcoming-ico/')
upcoming_SOUP = BeautifulSoup(upcoming_RESPONSE.text, 'html.parser')
all_tab = upcoming_SOUP.find(class_='col-lg-6 col-md-12 col-12 all')
upcoming_POSTS = all_tab.find_all(class_='col-md-12 col-12 a_ico')
for post in upcoming_POSTS:
    #print(post)
    name = post.find('div',class_='ico-main-info')
    if name is not None:
        project_name = name.find('a')
        project_name = project_name.get_text()
        print(project_name)
        project_link = name.find('a')['href']
        #print(project_link)
    upcoming_interest = post.find('div',class_='interest')
    if upcoming_interest is not None:
        interest = upcoming_interest.get_text().replace('\n', '').replace("\t","")
        #print(interest)
    upcoming_category = post.find('div',class_='categ_type')
    if upcoming_category is not None:
        category = upcoming_category.get_text().replace('\n', '').replace("\t","")
        #print(category)
    upcoming_start_date = post.find('div',class_='date')
    if upcoming_start_date is not None:
        start_date = upcoming_start_date.get_text().replace('\n', '').replace("\t","")
        #print(start_date)
    UPCOMING_HEADER_LINK_DF = UPCOMING_HEADER_LINK_DF.append({'Project' : project_name,
                                    'Project_Link':project_link,
                                    'INTEREST': interest,
                                    'CATEGORY': category,
                                    'START_DATE': start_date,
                                    'COLLECTED_DATE' : today
                                    }, ignore_index=True)
UPCOMING_HEADER_LINK_DF.to_csv("ico_drops_upcoming_projects.csv", index=False,encoding='utf-8-sig')


###
driver = webdriver.Chrome("C:/Users/hvvel/Downloads/Softwares/chromedriver_win32/chromedriver.exe") 
driver.get("https://icodrops.com/category/ended-ico/")
soup_num = BeautifulSoup(driver.page_source, "html.parser")
all_num = soup_num.find(class_='active_tab_category').find('sub').get_text()

time.sleep(7)  # Allow 2 seconds for the web page to open
scroll_pause_time = 10 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
screen_height = 5*driver.execute_script("return window.screen.height;")   # get the screen height of the web
i = 1

while True:
    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
#    scroll_height = driver.execute_script("return document.body.scrollHeight;")*2
    soup = BeautifulSoup(driver.page_source, "html.parser")
    all_tab = soup.find(class_='col-lg-6 col-md-12 col-12 all')
    ended_POSTS = all_tab.find_all(class_='col-md-12 col-12 a_ico')     
    print(i, '---', len(ended_POSTS))
    if (len(ended_POSTS) == 742):
        break
    
soup = BeautifulSoup(driver.page_source, "html.parser")
all_tab = soup.find(class_='col-lg-6 col-md-12 col-12 all')
ended_POSTS = all_tab.find_all(class_='col-md-12 col-12 a_ico')   
for post in ended_POSTS:
#print(post)
    name = post.find('div',class_='ico-main-info')
    if name is not None:
        project_name = name.find('a')   
        project_name = project_name.get_text()
        print(project_name)
        project_link = name.find('a')['href']
    #print(project_link)
    ended_interest = post.find('div',class_='interest')
    if ended_interest is not None:
        interest = ended_interest.get_text().replace('\n', '').replace("\t","")
        #print(interest)
    ended_category = post.find('div',class_='categ_type')
    if ended_category is not None:
        category = ended_category.get_text().replace('\n', '').replace("\t","")
        #print(category)
    upcoming_end_date = post.find('div',class_='date')
    if upcoming_end_date is not None:
        end_date = upcoming_end_date.get_text()
        if "Ended: " in end_date:
            end_date = end_date.replace("Ended: ","").replace('\n', '').replace("\t","")
            end_date = datetime.datetime.strptime(end_date,'%d %b %Y').strftime('%m/%d/%Y')
        #print(end_date)
    market = post.find(id= 't_tikcer', class_='nr yes tooltip')
    if market is not None:
        market_data = market.get_text().replace('\n', '').replace("\t","") 
        if "Ticker:" in market_data:
            market_data = market_data.replace("Ticker:","")
    ENDED_HEADER_LINK_DF = ENDED_HEADER_LINK_DF.append({'Project' : project_name,
                                    'Project_Link':project_link,
                                    'INTEREST': interest,
                                    'CATEGORY': category,
                                    'END_DATE': end_date,
                                    'MARKET_TICKER' : market_data,
                                    'COLLECTED_DATE' : today
                                    }, ignore_index=True)
ENDED_HEADER_LINK_DF.to_csv("ico_drops_ended_projects.csv", index=False,encoding='utf-8-sig')
#    if (screen_height) * i > scroll_height:
