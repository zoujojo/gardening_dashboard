
# -*- coding: utf-8 -*-
"""
Created on Thu May  5 16:12:11 2022
MA705 Final Project - Creating a Dashboard
@author: zoujo
"""

import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

PLANT_dir = "C:/Users/zoujo/OneDrive/Desktop/plant/"

stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=stylesheet)
server = app.server

# read data
df = pd.read_pickle(PLANT_dir + "zone6_plants.pkl")

df_selected = df[df["Exposure"].isin(["Full Sun"]) & 
                 df["Water Needs"].isin(["Average"]) &
                 df["Maintenance"].isin(["Average"])]

df_selected = df[(df["Exposure"] == "Partial Sun") & 
                 (df["Water Needs"] == "Average") &
                 (df["Maintenance"] == "Low")]


# read pie chart data
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
  - Light level - sun light levels, such as Full Sun, Partial Sun, Shade, or their combinations
  - Water needs - watering levels, such as Low, Average, High, or their combinations
  - Maintenance - the level of maintenance, including Low, Average, High
'''

markdown_text_use = '''
###### How to use this dashboard?
Please enter your search criteria below and the dashboard will display all plants, 
matching the criteria. Detailed information about the search results is 
presented in the table below, while the pie chart on the right shows the 
breakout of the search results by plant type. 

'''

app.layout = html.Div([
    html.H1('Gardening in Massachussetts',
            style={'textAlign' : 'left'}),
    dcc.Markdown(children=markdown_text_intr),
    html.Br(),
    
    
    html.Div(children=[
        dcc.Markdown(children=markdown_text_use),        
        html.Br(),
        
        html.Label('Select light level'),
        dcc.Dropdown(id='dropdown_1',
                     options=[{'label': i, 'value': i} for i in df.Exposure.unique()], 
                     value='Full Sun, Partial Sun'),
        html.Br(),
        
        html.Label('Select wather needs:',
                style={'textAlign' : 'left'}),
        dcc.Dropdown(id='dropdown_2',
                     options=[{'label': i, 'value': i} for i in df['Water Needs'].unique()], 
                     value='Average'),
        html.Br(),
        
        html.Label('Select maintenance:',
                style={'textAlign' : 'left'}),
        dcc.Dropdown(id='dropdown_3',
                     options=[{'label': i, 'value': i} for i in df.Maintenance.unique()], 
                     value='Low'),
        html.Br()
        
        ],
        style={'width' : '30%', 'float' : 'left'}),
    
    html.Div(children=[
       dcc.Graph(figure=fig, id='plot')],
        style={'width' : '70%', 'float' : 'right'}),
    
    html.Br(),
    
    html.Div(children=[
        html.H3('Search Results',
            style={'textAlign' : 'left'}),
        
        dash_table.DataTable(
            id="table",
            data=df.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in df.columns],
            page_size=20,  # we have less data in this example, so setting to 20
            fixed_rows={'headers': True},
            sort_action="native",
            style_table={'height': '300px', 'overflowY': 'auto'}
            #,style_cell={'minWidth': 95, 'maxWidth': 95, 'width': 95}
            )
        
       ],
        style={})
    ])

@app.callback(
    Output("table", "data"),
    [Input("dropdown_1", "value"),
    Input("dropdown_2", "value"),
    Input("dropdown_3", "value")]
)

def update_table(exposures, water_needs, maintenances):
    df_selected = df[(df["Exposure"] == exposures) & 
                     (df["Water Needs"] == water_needs) &
                     (df["Maintenance"] == maintenances)]
    # columns=[{'id': c, 'name': c} for c in df_selected.columns]
    data = df_selected.to_dict('records')
    return data

@app.callback(
    Output("plot", "figure"),
    [Input("dropdown_1", "value"),
    Input("dropdown_2", "value"),
    Input("dropdown_3", "value")]
)

def update_plot(exposures, water_needs, maintenances):
    df_selected = df[(df["Exposure"] == exposures) & 
                     (df["Water Needs"] == water_needs) &
                     (df["Maintenance"] == maintenances)]
    
    df_type = df_selected.groupby("Plant Type").count().reset_index().iloc[:,0:2]
    df_type = df_type.rename(columns={"Name": "Count"})
    
    fig = px.pie(df_type, values='Count', names='Plant Type')
    fig.update_traces(textposition='inside')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)




