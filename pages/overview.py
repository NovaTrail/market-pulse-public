
from dash import dcc, html
import numpy as np
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go

import pathlib
import dash_bootstrap_components as dbc  

# get parent directory path
path = pathlib.Path(__file__).parent.parent

# Read data sources
df = pd.read_csv(path.joinpath("data/PPIC_EU27_5ys.csv"))
dfcpi = pd.read_csv(path.joinpath("data/CPI_EU27_5ys.csv")) 

# ------------------------------------------------------------------------
# Create Graphs 
# ------------------------------------------------------------------------
# Graph 1 - CPI, PPI over last 5 years

dfcpi_a = dfcpi[(dfcpi['code']=='hcpi')]
dfcpi_b = dfcpi[(dfcpi['code']=='cpi_ctax')]
dfcpi_c = dfcpi[(dfcpi['code']=='ppi')]

fig = px.line()
fig.add_scatter(x=dfcpi_a['time'],y=dfcpi_a['index'],name='HCPI')
fig.add_scatter(x=dfcpi_c['time'],y=dfcpi_c['index'],name='PPI')

# Graph 2  - Heatmap of 
df_2y = df[df['time']>'2021-01']  
fig2 = go.Figure(data=go.Heatmap(
          x = df_2y['time'],
          y = df_2y['name'], 
          z = df_2y['index'],
          type = 'heatmap',
          zmin=-5,zmax=25,
          )) 

# Graphs 3 & 4 - heatmaps of 2 most inflationary and 2 most deflationary 
df = df[df['time']>'2021-05']

# Two most deflationary 
bottom2 = df.sort_values(by=['index'])['code'].unique()[0:2]
bottom2 = df[df['code'].isin(bottom2)]

# Two most Inflationary
top2 = df.sort_values(by=['index','code'],ascending=False)['code'].unique()[0:2] 
top2 = df[df['code'].isin(top2)]

fig3 = go.Figure(data=go.Heatmap(
          x = top2['time'],
          y = top2['name'], 
          z = top2['index'],
          type = 'heatmap',
          colorscale = 'sunsetdark',
          )) 

fig4 = go.Figure(data=go.Heatmap(
          x = bottom2['time'],
          y = bottom2['name'], 
          z = bottom2['index'],
          type = 'heatmap',
          colorscale = 'ice',
          ))

# ------------------------------------------------------------------------
# App layout
# ------------------------------------------------------------------------
layout = html.Div([
    dbc.Row([
        dbc.Col(width=1),
        dbc.Col([   
            html.Br(),  
            dbc.Card("Overview",color="info",inverse=True),

            dcc.Markdown("""
                        This interactive site uses data from Eurostat to analyse the inflationary and deflationary trends in consumer and producer prices.
                        #### Headline Inflation (HCPI) 
                        Here we see the change in Headline Consumer Price Index (CPI) and the harmonised Producer Price Index (PPI). 
                    """,style={'font-size': '16px','text-align': 'justify'}),
            
            dcc.Graph(id='map', figure=fig, config= {'displayModeBar': False}),
            dcc.Markdown("""
                        ### Heat map of PPI yoy increases
                        The PPI subcomponents (level 2) can be seen in the heatmap below. 
                    """,style={'font-size': '16px','text-align': 'justify'}),
            dcc.Graph(id='map', figure=fig2,config= {'displayModeBar': False}),

            dcc.Markdown("""
                        The next two heatmaps take a deeper look at the most inflationary and deflationary categories.
                        ### Two most inflationary PPI Categories
                    """,style={'font-size': '16px','text-align': 'justify'}),
            dcc.Graph(id='map', figure=fig3), 
            dcc.Markdown(""" ### Two most deflationary PPI Categories""",style={'font-size': '16px','text-align': 'justify'}),
            dcc.Graph(id='map2', figure=fig4),
            dcc.Markdown("""###### Continue to the [Prediction page](/insight)""",style={'font-size': '16px','text-align': 'justify'}),
            html.Hr(),
            html.P("About", id="about"),
            dcc.Markdown("This site was created as a hobby-level interest-project. The project is built on the Dash Framework using Python",style={'font-size': '16px','text-align': 'justify'}),
        
        ],
        width=10
        ),
        dbc.Col(width=1),
    ])
],style={"border":"10px white solid"})

