# gardening_dashboard - MA705 Final Project

This repository contains files used in the MA705 dashboard project - Gardening in Massachusetts Dashboard.

## Dashboard Description

This dashboard summarizes the gardening information from 664 plants for Massachusetts gardening purpose. It displays a data table to show the search results according to the users' three choices of light level, water needs, and maintenance of plants. A pie chart shows the breakout of the search results by plant type.

### Data Sources

The data source is https://www.gardenia.net. The data set is a subset by filtering three features -"Zone 6" in "Hardiness Zones", "Small Gardens" in "Garden Styles" and "United States" in "Regions" from the website.

All data is obtained by web scraping. The data type is string. Data is cleaned and a main data frame is saved in a pickle file. Another data frame with number of plants by plant type is created and saved in a pickle file.


### Reference:
- https://www.gardenia.net/plants/hardiness-zones/6
- https://www.gardeningknowhow.com/planting-zones/massachusetts-planting-zones.htm
- https://dash.plotly.com
- https://stackoverflow.com/questions/70205486/clickable-hyperlinks-in-plotly-dash-datatable

### Other Comments

The dashboard is under improving. 
