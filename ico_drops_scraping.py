# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 01:59:47 2021

@author: hvvel
"""
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 03:28:03 2021

@author: hvvel
"""

from bs4 import BeautifulSoup
from gis_metadata.metadata_parser import get_metadata_parser
from datetime import date
import os
import requests
import re
import time
import datetime
import pandas as pd
import metadata_parser



today = date.today()
today = today.strftime("%m/%d/%y")

start = time.time()

link_active = pd.read_csv(r"C:\Users\hvvel\OneDrive\Documents\RA\Final Code\ICO_DROPS\ico_drops_active_projects.csv",encoding='utf-8-sig')

link_ended = pd.read_csv(r"C:\Users\hvvel\OneDrive\Documents\RA\Final Code\ICO_DROPS\ico_drops_ended_projects.csv",encoding='utf-8-sig')

link_upcoming = pd.read_csv(r"C:\Users\hvvel\OneDrive\Documents\RA\Final Code\ICO_DROPS\ico_drops_upcoming_projects.csv",encoding='utf-8-sig')


drop_active = link_active["Project_Link"]

drop_ended = link_ended["Project_Link"]

drop_upcoming = link_upcoming["Project_Link"]

links = [*drop_active, *drop_ended, *drop_upcoming] 

OVERVIEW_HEADER = []
LISTDICT = []
brDict = {} 
for link in links: 
    RESPONSE = requests.get(link)
    SOUP = BeautifulSoup(RESPONSE.text, 'html.parser')
    post = SOUP.find(class_='col-12 col-lg-10')
    page = metadata_parser.MetadataParser(link)
    if page.get_metadatas('article:published_time') is not None:
        brDict['Proj_Publish_Date'] = page.get_metadatas('article:published_time')[0]
    if page.get_metadatas('article:modified_time') is not None:
        brDict['Proj_Modify_Date'] = page.get_metadatas('article:modified_time')[0]
    if page.get_metadatas('og:updated_time') is not None:
        brDict['Proj_Update_Date'] = page.get_metadatas('og:updated_time')[0]
    #for post in POSTS:
    #print(post)
    name = post.find('div',class_='ico-main-info')
    if name is not None:
        project_name = name.find('h3')
        project_name = project_name.get_text()
        print(project_name)
        brDict['Project'] = project_name
        brDict['Collected_Date'] = today
    notes = post.find('div',class_='important-note')
    if notes is not None:
        imp_text = notes.find('span',class_='red').next_sibling.string
        #print(imp_text)
        brDict['Imp_txt'] = imp_text
        i_link = notes.find('a')
        if i_link is not None:
            imp_link = i_link.get('href')
        #print(imp_link)
            brDict['Imp_link'] = imp_link
        othr = notes.find_all('br')
        for i in othr:
            #print(i.next_sibling)
            text = i.next_sibling
            if text is not None:
                key = text.string.strip().split('：')
                if(len(key) < 2):
                    key = text.string.strip().split(':')    
                if(len(key) == 2):
                    #print('--', key[0], '---', key[1])
                    brDict[key[0]] = key[1]
                elif len(key) == 1:
                    brDict['otherText'] = key[0]
    desc = post.find('div',class_='ico-description')
    if desc is not None:
        desc = desc.get_text().strip()
        #print(desc)
        brDict['Description'] = desc
    token_sale = post.find('div',class_='token-sale')
    if token_sale is not None:
        sale_date_high = token_sale.find(class_='sale-date')
        if sale_date_high is not None:
            sale_date = sale_date_high.get_text().strip()
            #print('sale date --- ',sale_date)
            brDict['Token Sale Date'] = sale_date
        token_sale_text = token_sale.find(text = True, recursive = False).strip()
        token_sale_status = token_sale.find('strong').find(text = True, recursive = False).strip()
        token_sale_2 = SOUP.find('div',class_='sale-date active')
        if token_sale_2 is not None:
            sale_date_2 = token_sale_2.get_text()     
            #print(token_sale_text)
            #print(token_sale_status) 
            brDict['token_sale_text'] = token_sale_status + sale_date_2
    LISTDICT.append(brDict)
    if len(OVERVIEW_HEADER) > 0:
        OVERVIEW_HEADER = list(set(OVERVIEW_HEADER+list(brDict.keys())))
    else:
        OVERVIEW_HEADER = list(brDict.keys())
    brDict = {}
PROJECT_OVERVIEW_DF_DROPS = pd.DataFrame(columns=OVERVIEW_HEADER)
for dictItem in LISTDICT:
    PROJECT_OVERVIEW_DF_DROPS = PROJECT_OVERVIEW_DF_DROPS.append(dictItem, ignore_index=True)
PROJECT_OVERVIEW_DF_DROPS.to_csv("PROJECT_OVERVIEW_DF_DROPS.csv", index=False,encoding='utf-8-sig')
        
#########
DETAIL_HEADER = []
NEWDICT = []
newDict = {}
for link in links:
    RESPONSE = requests.get(link)
    SOUP = BeautifulSoup(RESPONSE.text, 'html.parser')        
    proj_name = SOUP.find(class_='ico-main-info')
    if proj_name is not None:
        newDict['Project Name']  = proj_name.find('h3').get_text().strip()
        print(newDict['Project Name'])
    l_name = SOUP.find('div',class_='button')
    if l_name is not None:
        newDict['project_link'] = l_name.find_previous('a').get('href')
    money_goal = SOUP.find(class_='blue money-goal')
    if money_goal is not None:
        newDict['Money-Goal_Collected'] = money_goal.get_text().strip()
        #print(newDict['Money-Goal'])
    goal = SOUP.find(class_='goal')
    if goal is not None:
        if "GOAL" not in goal:
            money_goal = goal.get_text().strip().strip("OFof")
            l = money_goal.find("(")
            newDict['Money-Goal_Target'] = money_goal[:l].strip()
            newDict['Money-Goal_Percent_Achieved'] = money_goal[l:].strip("(,)")
        else:
            newDict['Money-Goal_Target'] = ""
            newDict['Money-Goal_Percent_Achieved'] = ""
    for l in SOUP.find_all('li'):
        if l.find('span', class_='grey') is not None:
            label = l.find('span', class_='grey')
            newDict[label.get_text().strip()] = label.next_sibling.string.strip()
    for ratingItem in SOUP.find_all(class_='rating-item'):
        #print(ratingItem)
        rating_box = ratingItem.find(class_='rating-box')
        key = rating_box.find('p').find(text=True, recursive=False).strip()
        newDict[key] = rating_box.find(class_='rate').get_text()
    ratingResult = SOUP.find(class_='rating-result')
    if ratingResult is not None:
        newDict['ICO Drops Score'] = ratingResult.find(class_='rating-box').find(class_='ico-rate').get_text()
    social_links = SOUP.find(class_='soc_links').find_all('a')
    if social_links is not None:
        for link in social_links:
            if len(link.find('i')['class']) > 1:
                social_platform = (link.find('i')['class'][1].split('-')[1])
                newDict[social_platform] = link.get('href')        
        newDict['Collected_Date'] = today
    NEWDICT.append(newDict)
    if len(DETAIL_HEADER) > 0:
        DETAIL_HEADER = list(set(DETAIL_HEADER+list(newDict.keys())))
    else:
        DETAIL_HEADER = list(newDict.keys())
    newDict = {}
PROJECT_DETAIL_DF_DROPS = pd.DataFrame(columns=DETAIL_HEADER)    
for dictItem in NEWDICT:
   PROJECT_DETAIL_DF_DROPS = PROJECT_DETAIL_DF_DROPS.append(dictItem, ignore_index=True)
PROJECT_DETAIL_DF_DROPS.to_csv("PROJECT_DETAIL_DF_DROPS.csv", index=False,encoding='utf-8-sig')
