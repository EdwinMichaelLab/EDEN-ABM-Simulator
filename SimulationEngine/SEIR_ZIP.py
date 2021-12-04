import plotly.express as px
import plotly.graph_objects as go
import  plotly as py
import pandas as pd
import sys
import numpy as np
import os
import geopandas as gpd
import pandas as pd
import plotly.express as px
import  plotly as py
from plotly.subplots import make_subplots
import os
from pyproj import Transformer
from shapely.geometry import Point
import math
import random
from datetime import datetime, date, timedelta, time
import queue
import threading
import time

def plot(df, zip):

    fig = go.Figure()

    # fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['susceptible'],
    #                          name="susceptible", line=dict({'width': 1, 'color': 'blue','dash':'dashdot'})), row=1, col=1)
    # fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vaccinated'],
    #                          name="vaccinated", line=dict({'width': 1, 'color': 'olive','dash':'dashdot'})), row=1, col=1)
    # fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['exposed'],
    #                          name="exposed", line=dict({'width': 1, 'color': 'orange','dash':'dashdot'})), row=1, col=1)
    # fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['asymptomatic'],
    #                          name="asymptomatic", line=dict({'width': 1, 'color': 'purple','dash':'dashdot'})), row=1, col=1)
    # fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['presymptomatic'],
    #                          name="presymptomatic", line=dict({'width': 1, 'color': 'red','dash':'dashdot'})), row=1, col=1)
    # fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['severe'],
    #                          name="severe", line=dict({'width': 1, 'color': 'darkred','dash':'dashdot'})), row=1, col=1)
    # fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['critical'],
    #                          name="critical", line=dict({'width': 1, 'color': 'crimson','dash':'dashdot'})), row=1, col=1)
    # fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['recovered'],
    #                          name="recovered", line=dict({'width': 1, 'color': 'green','dash':'dashdot'})), row=1, col=1)


    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['cases'],
                             name="cases", line=dict({'width':2, 'color':'red'})))
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vcases'],
                             name="vcases", line=dict({'width': 1.5, 'color': 'red', 'dash':'dot'})))


    # fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['admissions'],
    #                          name="admissions", line=dict({'width':2, 'color':'green'})), row=1, col=2)
    # fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vadmissions'],
    #                          name="actual admissions", line=dict({'width': 1.5, 'color': 'green', 'dash': 'dot'})), row=1, col=2)
    #
    # fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['dead'],
    #                          name="deaths", line=dict({'width': 2, 'color': 'black'})), row=1, col=3)
    # fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vdeaths'],
    #                          name="actual deaths", line=dict({'width': 1.5, 'color': 'black', 'dash': 'dot'})), row=1, col=3)
    # fig.update_traces(hoverinfo='text+name', mode='lines+markers')
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True, ticklabelmode="period", dtick="M1")
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_layout(title=zip, showlegend=True, autosize=True, width=1500, height=500,
                      legend=dict(orientation="h",x=0, y=-0.5, traceorder="normal"),
                      font=dict(family="Arial", size=12))
    # import plotly as py
    # py.offline.plot(fig, filename=os.path.join(os.path.dirname(os.getcwd()),
    #                                            'SEIR-' + datetime.now().strftime("%Y-%m-%d") + '.html'))
    fig.show()

path = os.path.join(os.path.dirname(os.getcwd()), 'SimulationEngine', 'output', '2021-11-18', 'final3')
print(path)
for root,dirs,files in os.walk(path):
    for file in files:
       if file.startswith("SEIR_"):
           zip = file.split('_')[1]
           df = pd.read_csv(os.path.join(root,file))
           start_step = 1
           startdate = datetime(2020, 3, 1)
           max = df['step'].max()
           steps = []
           for i in range(max):
               steps.append(i)

           validdf = pd.read_csv(
               os.path.join(os.path.dirname(os.getcwd()), 'SimulationEngine', 'input', 'hillsborough_dailycases.csv'))
           validdf = validdf.rename(columns={'cases': 'vcases',
                                             'admissions': 'vadmissions',
                                             'deaths': 'vdeaths'})

           records = []
           for step in steps:
               step = int(step)
               date = str((startdate + timedelta(days=step)).date())
               v = validdf.loc[validdf['date'] == date]
               if not v.empty:
                   vcases = validdf.loc[validdf['date'] == date, 'vcases'].values[0]
                   vadmissions = validdf.loc[validdf['date'] == date, 'vadmissions'].values[0]
                   vdeaths = validdf.loc[validdf['date'] == date, 'vdeaths'].values[0]

               d = df.loc[df['step'] == step]
               cases = d['presymptomatic'].sum() + d['mild'].sum()
               admissions = d['severe'].sum() + d['critical'].sum()

               dic = {'date': date,
                      'cases': cases,
                      'admissions': admissions,
                      'susceptible': d['susceptible'].values[0],
                      'vaccinated': d['vaccinated'].values[0],
                      'exposed': d['exposed'].values[0],
                      'asymptomatic': d['asymptomatic'].values[0],
                      'presymptomatic': d['presymptomatic'].values[0],
                      'mild': d['mild'].values[0],
                      'severe': d['severe'].values[0],
                      'critical': d['critical'].values[0],
                      'recovered': d['recovered'].values[0],
                      'dead': d['dead'].values[0],
                      'vcases': vcases,
                      'vadmissions': vadmissions,
                      'vdeaths': vdeaths}

               records.append(dic)

           plotdf = pd.DataFrame(records)
           plotdf = plotdf.sort_values(by='date')
           plot(plotdf, zip)