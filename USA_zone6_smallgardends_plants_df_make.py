# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 21:56:14 2022
MA705 Final Project - Data scaping, cleaning, & wrangling
@author: zoujo
"""

import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

# make folder for results
PLANT_dir = "C:/Users/zoujo/OneDrive/Desktop/plant/"
# os.mkdir(PLANT_dir)

# create a blank dataframe with 9 columns
COLUMN_NAME = ["Name", "Hardiness", "Plant Type", "Exposure", 
               "Season of Interest", "Water Needs", "Maintenance", 
               "Soil Type", "Soil Drainage", 
               "Garden Uses", "Link"]

plant_df = pd.DataFrame(columns = COLUMN_NAME)


# hardiness zone-5, region-USA, planting place-small gardens - total 38 pages

headers = {"User-Agent" : "Safari"}

# Function to collect row data by page
def get_page_data(zone_page_link):
    
    zone_5_req = requests.get(zone_page_link, headers=headers)
    zone_5_page1 = BeautifulSoup(zone_5_req.text, 'html.parser')

    page1_links = zone_5_page1.select('div[data-type="dashboard/content/plants"] a')
    len(page1_links)  # 60

    page1_plants_links = [link['href']
                    for link in page1_links if link.text=="Read More"]


    # add 15 plants in one page to dataframe
    for link in page1_plants_links:
        
        plant_name = link.split("/")[-1].replace("-", " ").title()
        length = len(plant_df)
        plant_df.loc[length, "Name"] = plant_name
        plant_df.loc[length, "Link"] = link
        
        
        table_req= requests.get(link, headers=headers)
        table_page = BeautifulSoup(table_req.text, 'html.parser')
        table = table_page.find('table')
        
        # Function to get one cell data
        def get_row_data(header):
            idx = [x.text for x in table.find_all('th')].index(header)
            value = table.find_all('td')[idx]
            row_data = value.text.replace('\n', ' ').replace('What\'s My Zone?', '').strip()
            return row_data
        
        # Add the cell data to dataframe
        for head in COLUMN_NAME[1:10]:
            length = len(plant_df)-1
            plant_df.loc[length, head] = get_row_data(head)
   
ZONE5_TOTAL_PAGE = 45

# page 1
USA_ZONE6_LINK = "https://www.gardenia.net/plants/hardiness-zones/6?RegionTerm=462&GardenElement=224&taxonomy=hardiness-zones&taxonomy_term=6&refine_for=refine_for_plants"

get_page_data(USA_ZONE6_LINK)

# page 2 to 45 pages
zone6_page_links = [USA_ZONE6_LINK + "&page="
                    + str(page) for page in range(2, ZONE5_TOTAL_PAGE+1)]

for page_link in zone6_page_links:
    get_page_data(page_link) 


# Display data
pd.set_option('display.max_columns', None)
plant_df.head()  # 45*15
plant_df.shape  # (664, 11)


plant_df.to_csv(PLANT_dir + 'zone6_plants.csv')

plant_df.to_pickle(PLANT_dir + 'zone6_plants.pkl',  protocol = 4)
