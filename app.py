
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

# df_selected = df[(df["Exposure"] == "Full Sun, Partial Sun") & 
#                   (df["Water Needs"] == "Average") &
#                   (df["Maintenance"] == "Low")]
# df_selected['Link'] = ['(' + link + ')' for link in df_selected.Link]

# df_type = df_selected.groupby("Plant Type").count().reset_index().iloc[:,0:2]
# df_type = df_type.rename(columns={"Name": "Count"})

# sum(df_type.Count)

# read pie chart data
df_type = pd.read_pickle(PLANT_dir + "plant_type_count.pkl")

# pie chart
fig = px.pie(df_type, values='Count', names='Plant Type')
fig.update_traces(textposition='inside')
fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')


markdown_text_intr = '''
The USDA released a plant hardiness map for 2012 that reflects average winter 
low temperatures over the last 30 years. You can find Massachusetts hardiness zone map 
[here](https://www.gardeningknowhow.com/wp-content/uploads/2004/10/massachusetts_map_lg.gif).
This dashboard summarizes the gardening information about 664 plants suitable 
for planting in hardiness zone 6. 
It allows an user to find plants for a small garden based on three search criteria, 
Light Level, Water Needs, and Maintenance. 
More information can be found at https://www.gardenia.net. 
'''

markdown_text_use = '''
Please select your search criteria below. Detailed information about the search results is 
presented in the table below. The pie chart on the right shows the 
breakout of the search results by plant type.
'''

app.layout = html.Div([
    html.Div([html.H1('Gardening in Massachussetts', 
                       style={'textAlign' : 'left', 'color': 'Green'}),
             
              dcc.Markdown(children=markdown_text_intr),
              html.Br()
              ]),
    
    
    html.Div(
             children=[
                 html.Label('How to use this dashboard?',
                           style={'textAlign' : 'left', "font-weight": "bold",
                                  'color': 'Green', "font-size": '17px'}),
                 dcc.Markdown(children=markdown_text_use),        
                 html.Br(),
        
                html.P('Select light level', 
                           style={'textAlign' : 'left'}),
                dcc.Dropdown(id='dropdown_1', 
                             options=[{'label': i, 'value': i} for i in df.Exposure.unique()], 
                             value='Full Sun, Partial Sun'),
                html.Br(),
        
                html.P('Select wather needs:', 
                           style={'textAlign' : 'left'}),
                dcc.Dropdown(id='dropdown_2',
                             options=[{'label': i, 'value': i} for i in df['Water Needs'].unique()], 
                             value='Average'),
                html.Br(),
        
                html.P('Select maintenance:', 
                           style={'textAlign' : 'left'}),
                dcc.Dropdown(id='dropdown_3',
                             options=[{'label': i, 'value': i} for i in df.Maintenance.unique()], 
                             value='Low')
                ],
             style={'width': '40%', 'float' : 'left', 'display': 'inline-block'}),
    
    html.Div( 
             children=[
                 html.H5( 
                         children=[
                         "There are ",
                         html.Span(id='output_box', children=''),
                         " plants matching your search criteria."],
                         style={'textAlign' : 'Center'}),
                 
                 # html.P(id='err'),
                 dcc.Graph(figure=fig, id='plot')], 
             
             style={'width': '60%', 'float' : 'right', 'display': 'inline-block'}),
    
    html.Div( 
             children=[
                 html.H3('Search Results', 
                         style={'textAlign' : 'left', 'color': 'Green'}),
                 html.Label('The results can be sorted by each column.'),
                 dash_table.DataTable(
                     id="table", 
                     data=df.to_dict('records'),
                     columns=[{'id': c, 'name': c, 'type': 'text', 'presentation': 'markdown'} 
                              if c == 'Link' else {'id': c, 'name': c} for c in df.columns],
                     
                     page_size=20,
                     fixed_rows={'headers': True},
                     sort_action="native",
                     style_table={'overflowX': 'auto'},
                     
                     style_cell={'textAlign': 'left', 
                                 'height': 'auto',
                                 # all three widths are needed
                                 'minWidth': '60px', 'width': '100px', 'maxWidth': '180px', 
                                 'whiteSpace': 'normal'},
                     
                     style_header={'textAlign': 'center', 
                                   'backgroundColor': 'LightGrey',
                                   'color': 'black',
                                   'fontWeight': 'bold'}
                     )
                 ],
             style={'display': 'inline-block'}),
    
    html.Br(),
    html.P('May 2022, Yun Zou')
    ], 
    
    style={'marginTop': 25,  'margin-right': 50, 'margin-left': 50})

@app.callback(
    [Output("table", "data"),
    Output("table", "columns")],
    [Input("dropdown_1", "value"),
    Input("dropdown_2", "value"),
    Input("dropdown_3", "value")]
)

def update_table(exposures, water_needs, maintenances):
    df_selected = df[(df["Exposure"] == exposures) & 
                     (df["Water Needs"] == water_needs) &
                     (df["Maintenance"] == maintenances)]
    # df_selected['Link'] = ['(' + link + ')' for link in df_selected.Link]
    
    columns=[{'id': c, 'name': c, 'type': 'text', 'presentation': 'markdown'} 
             if c == 'Link' else {'id': c, 'name': c} for c in df.columns]
    data = df_selected.to_dict('records')
    
    return data, columns

@app.callback(
    Output("plot", "figure"),
    # Output("err", "children"),
    Output("output_box", "children"),
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
    number = sum(df_type.Count)
    
    fig = px.pie(df_type, values='Count', names='Plant Type')
    fig.update_traces(textposition='inside')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    return fig, number
    


if __name__ == '__main__':
    app.run_server(debug=True)




