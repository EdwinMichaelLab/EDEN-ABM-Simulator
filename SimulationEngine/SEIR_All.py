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

def plot(df):
    sub_groups = ['Cases', 'Admissions', 'Deaths']
    fig = make_subplots(rows=1, cols=1, subplot_titles=sub_groups, vertical_spacing=0.01, horizontal_spacing=0.01,
                        shared_yaxes=True)

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
                             name="cases", line=dict({'width':2, 'color':'red'})), row=1, col=1)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vcases'],
                             name="vcases", line=dict({'width': 1.5, 'color': 'red', 'dash':'dot'})), row=1, col=1)

    # fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['original'],
    #                          name="original", line=dict({'width': 1.5, 'color': 'purple', 'dash': 'dot'})), row=1,
    #               col=1)
    # fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['delta'],
    #                          name="delta", line=dict({'width': 1.5, 'color': 'orange', 'dash': 'dot'})), row=1,
    #               col=1)
    # fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['lockdown'],
    #                          name="lockdown", line=dict({'width': 1.5, 'color': 'grey', 'dash': 'dot'})), row=1,
    #               col=1)



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
    fig.update_layout(showlegend=True, autosize=True, width=1500, height=500,
                      legend=dict(orientation="h",x=0, y=-0.5, traceorder="normal"),
                      font=dict(family="Arial", size=12))
    import plotly as py
    py.offline.plot(fig, filename=os.path.join(os.path.dirname(os.getcwd()),
                                               'SEIR-' + datetime.now().strftime("%Y-%m-%d") + '.html'))
    fig.show()

path = os.path.join(os.path.dirname(os.getcwd()), 'SimulationEngine', 'output', '2021-11-29', 'run1')
print(path)

validdf = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), 'SimulationEngine', 'input', 'hillsborough_dailycases.csv'))
validdf = validdf.rename(columns={'cases': 'vcases',
                                  'admissions': 'vadmissions',
                                  'deaths': 'vdeaths'})
variants = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), 'SimulationEngine', 'input', 'variants.csv'))
lockdown = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), 'SimulationEngine', 'input', 'lockdown.csv'))

startdate = date(2020, 3, 1)
enddate = date(2021, 12, 31)
steps = (enddate  - startdate).days + 1
dic = {}
for step in range(0,steps):
    step = int(step)
    date = str((startdate + timedelta(days=step)))
    v = validdf.loc[validdf['date'] == date]
    vcases = 0
    vadmissions = 0
    vdeaths = 0
    if not v.empty:
        vcases = validdf.loc[validdf['date'] == date, 'vcases'].values[0]
        vadmissions =  validdf.loc[validdf['date'] == date, 'vadmissions'].values[0]
        vdeaths =  validdf.loc[validdf['date'] == date, 'vdeaths'].values[0]

    vr = variants.loc[variants['date'] == date]
    original = 0
    delta = 0
    if not vr.empty:
        original = variants.loc[variants['date'] == date, 'original'].values[0]
        delta = variants.loc[variants['date'] == date, 'delta'].values[0]

    ld =  lockdown.loc[lockdown['date']==date]
    lckdwn = 0
    if not ld.empty:
        for index, row in ld.iterrows():
            for column in ld.columns:
                if column!='date':
                    lckdwn+= row[column]

    dic[step] = {
                'date': date,
                'susceptible': 0,
                'vaccinated': 0,
                'exposed': 0,
                'asymptomatic': 0,
                'presymptomatic': 0,
                'mild': 0,
                'severe': 0,
                'critical': 0,
                'recovered': 0,
                'dead': 0,
                'cases': 0,
                'admissions': 0,
                'vcases': vcases,
                'vadmissions': vadmissions,
                'vdeaths': vdeaths,
                'original': original*200000,
                'delta': delta * 200000,
                'lockdown': lckdwn * 10000
            }

for root,dirs,files in os.walk(path):
    for file in files:
       if file.startswith("SEIR_"):
           df = pd.read_csv(os.path.join(root,file))
           for index, row in df.iterrows():
               d = dic[row['step']]
               d['susceptible'] += row['susceptible']
               d['vaccinated'] += row['vaccinated']
               d['exposed'] += row['exposed']
               d['asymptomatic'] += row['asymptomatic']
               d['presymptomatic'] += row['presymptomatic']
               d['mild'] += row['mild']
               d['severe'] += row['severe']
               d['critical'] += row['critical']
               d['recovered'] += row['recovered']
               d['dead'] += row['dead']
               d['cases'] += row['presymptomatic'] + row['mild']
               d['admissions'] += row['severe'] + row['critical']

records = []
for step in range(0,steps):
    records.append(dic[step])

plotdf = pd.DataFrame(records)
plotdf = plotdf.sort_values(by='date')
plot(plotdf)
