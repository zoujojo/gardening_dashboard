# -*- coding: utf-8 -*-
"""
Created on Thu May  5 16:12:11 2022
MA705 Final Project - Creating a Dashboard
@author: zoujo
"""

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

PLANT_dir = "C:/Users/zoujo/OneDrive/Desktop/plant/"

stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

### pandas dataframe to html table
def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

app = dash.Dash(__name__, external_stylesheets=stylesheet)
server = app.server

df = pd.read_pickle(PLANT_dir + "zone6_plants.pkl")

df_type = pd.read_pickle(PLANT_dir + "plant_type_count.pkl")


# pie chart
fig = px.pie(df_type, values='Count', names='Plant Type')
fig.update_traces(textposition='inside')
fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')


markdown_text_intr = '''
###### Instroduction about the dashboard 

The USDA released a plant hardiness map for 2012 that reflects average winter 
low temperatures over the last 30 years. The Massachussets planting map includes zone 5 to 7. 
This dashboard summarizes the gardening information from 664 plants in hardiness zone 6. 
You can find the data source [here](https://www.gardenia.net/plants/hardiness-zones/6). 
It allows an user to find plants for a small garden based on the following 
three search criteria:
- Light level - sun light levels, such as Full Sun, Partial Sun, Shade, or their combinations
- Water needs - watering levels, such as Low, Average, High, or their combinations
- Maintenance - the level of maintenance, including Low, Average, High

'''

markdown_text_use = '''
###### How to use this dashboard?
Please select your search criteria below and the dashboard will display all plants, 
matching the criteria. Detailed information about the search results is 
presented in the table below, while the pie chart on the right shows the 
breakout of the search results by plant type. 
'''

app.layout = html.Div([
    html.H1('Gardening in Massachusetts Dashboard',
            style={'textAlign' : 'left'}),
    dcc.Markdown(children=markdown_text_intr),
    html.Br(),
    
    
    html.Div(children=[
        dcc.Markdown(children=markdown_text_use),
        'Select a light level:',
        dcc.Dropdown(options=[{'label': 'Full Sun', 'value': 'Full Sun'},
                 {'label': 'Full Sun, Partial Sun', 'value': 'Full Sun, Partial Sun'},
                 {'label': 'Full Sun, Partial Sun, Shade', 'value': 'Full Sun, Partial Sun, Shade'},
                 {'label': 'Partial Sun', 'value': 'Partial Sun'},
                 {'label': 'Partial Sun, Shade', 'value': 'Partial Sun, Shade'}],
                  id='dropdown-1', value = ["Full Sun"]),
                  # value=['Full Sun', 'Full Sun, Partial Sun', 
                  #        'Full Sun, Partial Sun, Shade',
                  #        'Partial Sun', 'Partial Sun, Shade']),

        html.Br(),
        
        'Select water needs:',
        dcc.Dropdown(options=[{'label': 'Average', 'value': 'Average'},
                              {'label': 'Low, Average', 'value': 'Low, Average'},
                              {'label': 'High', 'value': 'High'},
                              {'label': 'Average, High', 'value': 'Average, High'},
                              {'label': 'Low', 'value': 'Low'}], 
                     id='dropdown-2', value=["Average"]),
                     # value=['Average', 'Low', 'High', 'Low, Average', 'Average, High']),

        html.Br(),
        
        html.Label('Select maintenance level'),
        dcc.Dropdown(options=[{'label': 'High', 'value': 'High'},
                              {'label': 'Average', 'value': 'Average'},
                              {'label': 'Low', 'value': 'Low'}], 
                     id='dropdown-3', value=["Average"])],
                     # value=[ 'Average', 'Low', 'High'])],
        style={'width' : '40%', 'float' : 'left'}),
    
    html.Div(children=[
       dcc.Graph(figure=fig, id='plot')],
        style={'width' : '60%', 'float' : 'right'}),
    
    html.Br(),
    
    html.H3('Search Results',
        style={'textAlign' : 'left'}),
    
    html.Div(children=[
        html.Div(id='table')])
    ])

@app.callback(
    Output("table", "children"),
    [Input("dropdown-1", "value"),
    Input("dropdown-2", "value"),
    Input("dropdown-3", "value")]
)
def update_table(Exposures, Water_Needs, Maintenances):
    x = df[df.Exposure.isin(Exposures)]
    x1 = x[x['Water Needs'].isin(Water_Needs)]
    x2 =  x1[x1.Maintenance.isin(Maintenances)]
    return generate_table(x2)

@app.callback(
    Output("plot", "figure"),
    [Input("dropdown-1", "value"),
    Input("dropdown-2", "value"),
    Input("dropdown-3", "value")]
)
def update_plot(Exposures, Water_Needs, Maintenances):
    # df1 = df[df.Exposure.isin(Exposures) and df['Water Needs'].isin(Water_Needs) 
    #        and df.Maintenance.isin(Maintenances)]
    x = df[df.Exposure.isin(Exposures)]
    x1 = x[x['Water Needs'].isin(Water_Needs)]
    x2 =  x1[x1.Maintenance.isin(Maintenances)]
    
    df_type = x2.groupby("Plant Type").count().reset_index().iloc[:,0:2]
    df_type = df_type.rename(columns={"Name": "Count"})
    
    fig = px.pie(df_type, values='Count', names='Plant Type')
    fig.update_traces(textposition='inside')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

if __name__ == '__main__':
    app.run_server(debug=True)




