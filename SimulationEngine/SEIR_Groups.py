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

def plot(vdf, min, mean, max):
    sub_groups = ['Cases', 'Admissions', 'Deaths']
    fig = make_subplots(rows=3, cols=1, subplot_titles=sub_groups, vertical_spacing=0.1, horizontal_spacing=0.01)
                        #shared_yaxes=True)

    # fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['susceptible'],
    #                          name="susceptible", line=dict({'width':  0.5, 'color': 'blue','dash':'dashdot'})), row=1, col=1)
    # fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vaccinated'],
    #                          name="vaccinated", line=dict({'width':  1.5, 'color': 'green','dash':'dashdot'})), row=1, col=1)
    #
    # fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['boosted'],
    #                          name="vaccinated", line=dict({'width': 1.5, 'color': 'olive', 'dash': 'dashdot'})), row=2,
    #               col=1)
    # fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['wanning'],
    #                          name="wanning", line=dict({'width': 1.5, 'color': 'grey', 'dash': 'dashdot'})), row=3,
    #               col=1)

    # fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['exposed'],
    #                          name="exposed", line=dict({'width':  0.5, 'color': 'orange','dash':'dashdot'})), row=1, col=1)
    # fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['asymptomatic'],
    #                          name="asymptomatic", line=dict({'width':  0.5, 'color': 'purple','dash':'dashdot'})), row=1, col=1)
    # fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['presymptomatic'],
    #                          name="presymptomatic", line=dict({'width':  0.5, 'color': 'red','dash':'dashdot'})), row=1, col=1)
    # fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['severe'],
    #                          name="severe", line=dict({'width':  0.5, 'color': 'darkred','dash':'dashdot'})), row=1, col=1)
    # fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['critical'],
    #                          name="critical", line=dict({'width':  0.5, 'color': 'crimson','dash':'dashdot'})), row=1, col=1)
    # fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['recovered'],
    #                          name="recovered", line=dict({'width':  0.5, 'color': 'green','dash':'dashdot'})), row=1, col=1)
    #

    fig.add_trace(go.Scatter(mode='lines', x=vdf['date'], y=mean['cases'],
                             name="cases", line=dict({'width': 2, 'color': 'red'})), row=1, col=1)
    fig.add_trace(go.Scatter(mode='lines', x=vdf['date'], y=min['cases'],
                             name="cases", fillcolor='rgba(255,153,204,0.5)', fill='tonexty', line=dict({'width':1, 'color':'rgba(255,153,204,1)'})), row=1, col=1)
    fig.add_trace(go.Scatter(mode='lines', x=vdf['date'], y=max['cases'],
                             name="cases", fillcolor='rgba(255,153,204,0.5)',  fill='tonexty', line=dict({'width':1, 'color':'rgba(255,153,204,1)'})), row=1, col=1)
    fig.add_trace(go.Scatter(mode='lines', x=vdf['date'], y=vdf['vcases'],
                             name="vcases", line=dict({'width':  2, 'color': 'red', 'dash':'dot'})), row=1, col=1)

    fig.add_trace(go.Scatter(mode='lines', x=vdf['date'], y=mean['admissions'],
                             name="admissions", line=dict({'width': 2, 'color': 'green'})), row=2, col=1)
    fig.add_trace(go.Scatter(mode='lines', x=vdf['date'], y=min['admissions'],
                             name="admissions", fillcolor='rgba(204,255,204,0.75)', fill='tonexty', line=dict({'width':1, 'color':'rgba(204,255,204,1)'})), row=2, col=1)
    fig.add_trace(go.Scatter(mode='lines', x=vdf['date'], y=max['admissions'],
                             name="admissions", fillcolor='rgba(204,255,204,0.75)', fill='tonexty', line=dict({'width':1, 'color':'rgba(204,255,204,1)'})), row=2, col=1)
    fig.add_trace(go.Scatter(mode='lines', x=vdf['date'], y=vdf['vadmissions'],
                             name="actual admissions", line=dict({'width':  2, 'color': 'green', 'dash': 'dot'})), row=2, col=1)

    fig.add_trace(go.Scatter(mode='lines', x=vdf['date'], y=mean['dead'],
                         name="deaths", line=dict({'width': 2, 'color': 'black'})), row=3, col=1)
    fig.add_trace(go.Scatter(mode='lines', x=vdf['date'], y=min['dead'],
                             name="deaths", fillcolor='rgba(192,192,192,0.75)', fill='tonexty', line=dict({'width':  1, 'color': 'rgba(192,192,192,1)'})), row=3, col=1)
    fig.add_trace(go.Scatter(mode='lines', x=vdf['date'], y=max['dead'],
                             name="deaths", fillcolor='rgba(192,192,192,0.75)', fill='tonexty', line=dict({'width':  1, 'color': 'rgba(192,192,192,1)'})), row=3, col=1)
    fig.add_trace(go.Scatter(mode='lines', x=vdf['date'], y=vdf['vdeaths'],
                             name="actual deaths", line=dict({'width':  2, 'color': 'black', 'dash': 'dot'})), row=3, col=1)
    fig.update_traces(hoverinfo='text+name')
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True, ticklabelmode="period", dtick="M1")
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_layout(showlegend=True, autosize=True, width=1000, height=1300,
                      legend=dict(orientation="h",x=0, y=-0.5, traceorder="normal"),
                      font=dict(family="Arial", size=12))
    import plotly as py
    py.offline.plot(fig, filename=os.path.join(os.path.dirname(os.getcwd()),
                                               'Actual-' + datetime.now().strftime("%Y-%m-%d") + '.html'))
    fig.show()


def plot_age(df):
    sub_groups = ['Cases >65', 'Admissions >65', 'Deaths >65', 'Cases >18', 'Admissions >18', 'Deaths >18',
                  'Cases >1', 'Admissions >1', 'Deaths >1']
    fig = make_subplots(rows=3, cols=3, subplot_titles=sub_groups, vertical_spacing=0.2, horizontal_spacing=0.02,
                        shared_yaxes=True)

    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['cases_65'],
                             name="cases >65", line=dict({'width': 2, 'color': 'red'})), row=1, col=1)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vcases'],
                             name="actual cases", line=dict({'width': 1.5, 'color': 'red', 'dash': 'dot'})), row=1,
                  col=1)
    # -------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['admissions_65'],
                             name="admissions >65", line=dict({'width': 2, 'color': 'green'})), row=1, col=2)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vadmissions'],
                             name="actual admissions", line=dict({'width': 1.5, 'color': 'green', 'dash': 'dot'})),
                  row=1, col=2)
    # -------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['deaths_65'],
                             name="deaths >65", line=dict({'width': 2, 'color': 'black'})), row=1, col=3)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vdeaths'],
                             name="actual deaths", line=dict({'width': 1.5, 'color': 'black', 'dash': 'dot'})),
                  row=1, col=3)
    # -------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['cases_18'],
                             name="cases >18", line=dict({'width': 2, 'color': 'red'})), row=2, col=1)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vcases'],
                             name="actual cases", line=dict({'width': 1.5, 'color': 'red', 'dash': 'dot'})), row=2,
                  col=1)
    # -------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['admissions_18'],
                             name="admissions >18", line=dict({'width': 2, 'color': 'green'})), row=2, col=2)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vadmissions'],
                             name="actual admissions", line=dict({'width': 1.5, 'color': 'green', 'dash': 'dot'})),
                  row=2, col=2)
    # -------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['deaths_18'],
                             name="deaths >18", line=dict({'width': 2, 'color': 'black'})), row=2, col=3)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vdeaths'],
                             name="actual deaths", line=dict({'width': 1.5, 'color': 'black', 'dash': 'dot'})),
                  row=2,
                  col=3)
    # -------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['cases_1'],
                             name="cases >1", line=dict({'width': 2, 'color': 'red'})), row=3, col=1)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vcases'],
                             name="actual cases", line=dict({'width': 1.5, 'color': 'red', 'dash': 'dot'})), row=3,
                  col=1)
    # -------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['admissions_1'],
                             name="admissions >1", line=dict({'width': 2, 'color': 'green'})), row=3, col=2)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vadmissions'],
                             name="actual admissions", line=dict({'width': 1.5, 'color': 'green', 'dash': 'dot'})),
                  row=3, col=2)
    # -------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['deaths_1'],
                             name="deaths >1", line=dict({'width': 2, 'color': 'black'})), row=3, col=3)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vdeaths'],
                             name="actual deaths", line=dict({'width': 1.5, 'color': 'black', 'dash': 'dot'})),
                  row=3,
                  col=3)
    # -------------------------------------------------------------------------------------------------------------------

    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True, ticklabelmode="period", dtick="M1")
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True, range=[0, 1000])
    fig.update_layout(showlegend=True, autosize=True,  height=1000,
                      legend=dict(orientation="h", x=0, y=-0.5, traceorder="normal"),
                      font=dict(family="Arial", size=12))

    py.offline.plot(fig, filename=os.path.join(os.path.dirname(os.getcwd()), 'SEIRbyAge-' + datetime.now().strftime("%Y-%m-%d")+ '.html'))
    fig.show()

def plot_race(df):
    sub_groups = ['Cases (white)', 'Admissions (white)', 'Deaths (white)',
                  'Cases (black)', 'Admissions (black)', 'Deaths (black)',
                  'Cases (asian)', 'Admissions (asian)', 'Deaths (asian)',
                  'Cases (other)', 'Admissions (other)', 'Deaths (other)',
                  'Cases (two)', 'Admissions (two)', 'Deaths (two)'
                  ]
    fig = make_subplots(rows=5, cols=3, subplot_titles=sub_groups, vertical_spacing=0.1, horizontal_spacing=0.02,
                        shared_yaxes=True)

    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['cases_white'],
                             name="Cases (white)", line=dict({'width': 2, 'color': 'red'})), row=1, col=1)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vcases'],
                             name="actual cases", line=dict({'width': 1.5, 'color': 'red', 'dash': 'dot'})), row=1,
                  col=1)
    # -------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['admissions_white'],
                             name="admissions (white)", line=dict({'width': 2, 'color': 'green'})), row=1, col=2)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vadmissions'],
                             name="actual admissions", line=dict({'width': 1.5, 'color': 'green', 'dash': 'dot'})),
                  row=1, col=2)
    # -------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['deaths_white'],
                             name="deaths (white)", line=dict({'width': 2, 'color': 'black'})), row=1, col=3)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vdeaths'],
                             name="actual deaths", line=dict({'width': 1.5, 'color': 'black', 'dash': 'dot'})), row=1,
                  col=3)
    # -------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['cases_black'],
                             name="cases (black)", line=dict({'width': 2, 'color': 'red'})), row=2, col=1)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vcases'],
                             name="actual cases", line=dict({'width': 1.5, 'color': 'red', 'dash': 'dot'})), row=2,
                  col=1)
    # -------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['admissions_black'],
                             name="admissions (black)", line=dict({'width': 2, 'color': 'green'})), row=2, col=2)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vadmissions'],
                             name="actual admissions", line=dict({'width': 1.5, 'color': 'green', 'dash': 'dot'})),
                  row=2, col=2)
    # -------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['deaths_black'],
                             name="deaths (black)", line=dict({'width': 2, 'color': 'black'})), row=2, col=3)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vdeaths'],
                             name="actual deaths", line=dict({'width': 1.5, 'color': 'black', 'dash': 'dot'})), row=2,
                  col=3)
    # -------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['cases_asian'],
                             name="cases (asian)", line=dict({'width': 2, 'color': 'red'})), row=3, col=1)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vcases'],
                             name="actual cases", line=dict({'width': 1.5, 'color': 'red', 'dash': 'dot'})), row=3,
                  col=1)
    # -------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['admissions_asian'],
                             name="admissions (asian)", line=dict({'width': 2, 'color': 'green'})), row=3, col=2)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vadmissions'],
                             name="actual admissions", line=dict({'width': 1.5, 'color': 'green', 'dash': 'dot'})),
                  row=3, col=2)
    # -------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['deaths_asian'],
                             name="deaths (asian)", line=dict({'width': 2, 'color': 'black'})), row=3, col=3)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vdeaths'],
                             name="actual deaths", line=dict({'width': 1.5, 'color': 'black', 'dash': 'dot'})), row=3,
                  col=3)
    # -------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['cases_other'],
                             name="cases (other)", line=dict({'width': 2, 'color': 'red'})), row=4, col=1)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vcases'],
                             name="actual cases", line=dict({'width': 1.5, 'color': 'red', 'dash': 'dot'})), row=4,
                  col=1)
    # -------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['admissions_other'],
                             name="admissions (other)", line=dict({'width': 2, 'color': 'green'})), row=4, col=2)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vadmissions'],
                             name="actual admissions", line=dict({'width': 1.5, 'color': 'green', 'dash': 'dot'})),
                  row=4, col=2)
    # -------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['deaths_other'],
                             name="deaths (other)", line=dict({'width': 2, 'color': 'black'})), row=4, col=3)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vdeaths'],
                             name="actual deaths", line=dict({'width': 1.5, 'color': 'black', 'dash': 'dot'})), row=4,
                  col=3)
    # -------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['cases_two'],
                             name="cases (two)", line=dict({'width': 2, 'color': 'red'})), row=5, col=1)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vcases'],
                             name="actual cases", line=dict({'width': 1.5, 'color': 'red', 'dash': 'dot'})), row=5,
                  col=1)
    # -------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['admissions_two'],
                             name="admissions (two)", line=dict({'width': 2, 'color': 'green'})), row=5, col=2)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vadmissions'],
                             name="actual admissions", line=dict({'width': 1.5, 'color': 'green', 'dash': 'dot'})),
                  row=5, col=2)
    # -------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['deaths_two'],
                             name="deaths (two)", line=dict({'width': 2, 'color': 'black'})), row=5, col=3)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vdeaths'],
                             name="actual deaths", line=dict({'width': 1.5, 'color': 'black', 'dash': 'dot'})), row=5,
                  col=3)
    # -------------------------------------------------------------------------------------------------------------------
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True, ticklabelmode="period", dtick="M1")
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True, range=[0, 1000])
    fig.update_layout(showlegend=True, autosize=True,  height=1800,
                      legend=dict(orientation="h", x=0, y=-0.5, traceorder="normal"),
                      font=dict(family="Arial", size=12))

    py.offline.plot(fig, filename=os.path.join(os.path.dirname(os.getcwd()), 'SEIRbyRace-' + datetime.now().strftime("%Y-%m-%d")+ '.html'))
    fig.show()

def plot_FPL(df):
    sub_groups = ['Cases (0-100)', 'Admissions (0-100)', 'Deaths (0-100)',
                  'Cases (100-150)', 'Admissions (100-150)', 'Deaths (100-150)',
                  'Cases (150-175)', 'Admissions (150-175)', 'Deaths (150-175)',
                  'Cases (175-200)', 'Admissions (175-200)', 'Deaths (175-200)',
                  'Cases (200-1800)', 'Admissions (200-1800)', 'Deaths (200-1800)'
                  ]
    fig = make_subplots(rows=5, cols=3, subplot_titles=sub_groups, vertical_spacing=0.1, horizontal_spacing=0.02,
                        shared_yaxes=True)

    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['cases_0-100'],
                             name="Cases (0-100)", line=dict({'width':2, 'color':'red'})), row=1, col=1)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vcases'],
                             name="actual cases", line=dict({'width': 1.5, 'color': 'red', 'dash':'dot'})), row=1, col=1)
    #-------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['admissions_0-100'],
                             name="admissions (0-100)", line=dict({'width':2, 'color':'green'})), row=1, col=2)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vadmissions'],
                             name="actual admissions", line=dict({'width': 1.5, 'color': 'green', 'dash': 'dot'})), row=1, col=2)
    # -------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['deaths_0-100'],
                             name="deaths (0-100)", line=dict({'width': 2, 'color': 'black'})), row=1, col=3)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vdeaths'],
                             name="actual deaths", line=dict({'width': 1.5, 'color': 'black', 'dash': 'dot'})), row=1, col=3)
    # -------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['cases_100-150'],
                             name="cases (100-150)", line=dict({'width': 2, 'color': 'red'})), row=2, col=1)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vcases'],
                             name="actual cases", line=dict({'width': 1.5, 'color': 'red', 'dash': 'dot'})), row=2,
                  col=1)
    # -------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['admissions_100-150'],
                             name="admissions (100-150)", line=dict({'width': 2, 'color': 'green'})), row=2, col=2)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vadmissions'],
                             name="actual admissions", line=dict({'width': 1.5, 'color': 'green', 'dash': 'dot'})),
                  row=2, col=2)
    # -------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['deaths_100-150'],
                             name="deaths (100-150)", line=dict({'width': 2, 'color': 'black'})), row=2, col=3)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vdeaths'],
                             name="actual deaths", line=dict({'width': 1.5, 'color': 'black', 'dash': 'dot'})), row=2,
                  col=3)
    # -------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['cases_150-175'],
                             name="cases (150-175)", line=dict({'width': 2, 'color': 'red'})), row=3, col=1)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vcases'],
                             name="actual cases", line=dict({'width': 1.5, 'color': 'red', 'dash': 'dot'})), row=3,
                  col=1)
    # -------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['admissions_150-175'],
                             name="admissions (150-175)", line=dict({'width': 2, 'color': 'green'})), row=3, col=2)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vadmissions'],
                             name="actual admissions", line=dict({'width': 1.5, 'color': 'green', 'dash': 'dot'})),
                  row=3, col=2)
    # -------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['deaths_150-175'],
                             name="deaths (150-175)", line=dict({'width': 2, 'color': 'black'})), row=3, col=3)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vdeaths'],
                             name="actual deaths", line=dict({'width': 1.5, 'color': 'black', 'dash': 'dot'})), row=3,
                  col=3)
    # -------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['cases_175-200'],
                             name="cases (175-200)", line=dict({'width': 2, 'color': 'red'})), row=4, col=1)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vcases'],
                             name="actual cases", line=dict({'width': 1.5, 'color': 'red', 'dash': 'dot'})), row=4,
                  col=1)
    # -------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['admissions_175-200'],
                             name="admissions (175-200)", line=dict({'width': 2, 'color': 'green'})), row=4, col=2)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vadmissions'],
                             name="actual admissions", line=dict({'width': 1.5, 'color': 'green', 'dash': 'dot'})),
                  row=4, col=2)
    # -------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['deaths_175-200'],
                             name="deaths (175-200)", line=dict({'width': 2, 'color': 'black'})), row=4, col=3)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vdeaths'],
                             name="actual deaths", line=dict({'width': 1.5, 'color': 'black', 'dash': 'dot'})), row=4,
                  col=3)
    # -------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['cases_200-1800'],
                             name="cases (200-1800)", line=dict({'width': 2, 'color': 'red'})), row=5, col=1)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vcases'],
                             name="actual cases", line=dict({'width': 1.5, 'color': 'red', 'dash': 'dot'})), row=5,
                  col=1)
    # -------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['admissions_200-1800'],
                             name="admissions (200-1800)", line=dict({'width': 2, 'color': 'green'})), row=5, col=2)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vadmissions'],
                             name="actual admissions", line=dict({'width': 1.5, 'color': 'green', 'dash': 'dot'})),
                  row=5, col=2)
    # -------------------------------------------------------------------------------------------------------------------
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['deaths_200-1800'],
                             name="deaths (200-1800)", line=dict({'width': 2, 'color': 'black'})), row=5, col=3)
    fig.add_trace(go.Scatter(mode='lines', x=df['date'], y=df['vdeaths'],
                             name="actual deaths", line=dict({'width': 1.5, 'color': 'black', 'dash': 'dot'})), row=5,
                  col=3)
    # -------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------------------------

    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True, ticklabelmode="period", dtick="M1")
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True, range=[0, 1000])
    fig.update_layout(showlegend=True, autosize=True,  height=1800,
                      legend=dict(orientation="h",x=0, y=-0.5, traceorder="normal"),
                      font=dict(family="Arial", size=12))

    py.offline.plot(fig, filename=os.path.join(os.path.dirname(os.getcwd()), 'SEIRbyFPL-' + datetime.now().strftime("%Y-%m-%d")+ '.html'))
    fig.show()


def load_SEIR(mode, pop, household):
    plotdf = pd.DataFrame(records)
    plotdf = plotdf.sort_values(by='date')
    if mode == 'All':
        return plot(plotdf)
    elif mode == 'ByAge':
        return plot_age(plotdf)
    elif mode == 'ByRace':
        return plot_race(plotdf)
    elif mode == 'ByFPL':
        return plot_FPL(plotdf)

code_dir = '' #'ABM-Simulator'
mode = 'ByAge' # 'All', 'ByAge', 'ByRace', 'ByFPL'
# path = os.path.join(os.path.dirname(os.getcwd()), code_dir, 'SimulationEngine', 'output', '2021-11-23', '0')
# print(path)
# pop = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), code_dir, 'SimulationEngine', 'input', 'persons.csv'))
# households = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), code_dir, 'SimulationEngine', 'input', 'households3.csv'))
# validdf = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), code_dir, 'SimulationEngine', 'input',  'hillsborough_dailycases.csv'))
# validdf = validdf.rename(columns={'cases': 'vcases','admissions': 'vadmissions','deaths': 'vdeaths'})
#
# dlist = []
# for root, dirs, files in os.walk(path):
#     for file in files:
#         if file.endswith(".csv"):
#             no = file.split('_')[1].split('.')[0]
#             d = pd.read_csv(os.path.join(root, file))
#             d['chunk'] = no
#             dlist.append(d)
#
# df = pd.concat(dlist)
# df = pd.merge(df, pop, on='pid')
# df = pd.merge(df, households, left_on='pid', right_on='occupant')
# df = df[(df['state']=='mild') | (df['state']=='severe') | (df['state']=='critical') | (df['state']=='dead') |
#             (df['state']=='presymptomatic') | (df['state']=='exposed')]
#
# start_step = 1
# startdate = datetime(2020, 3, 1)
# max = df['step'].max()
# steps = []
# for i in range(max):
#     steps.append(i)
#
# records = []
# for step in steps:
#     step = int(step)
#     date = str((startdate + timedelta(days=step)).date())
#     v = validdf.loc[validdf['date'] == date, 'vcases']
#     if not v.empty:
#         vcases = validdf.loc[validdf['date'] == date, 'vcases'].values[0]
#         vadmissions = validdf.loc[validdf['date'] == date, 'vadmissions'].values[0]
#         vdeaths = validdf.loc[validdf['date'] == date, 'vdeaths'].values[0]
#
#         dic = {'date': date,
#                'vcases': vcases,
#                'vadmissions': vadmissions,
#                'vdeaths': vdeaths}
#
#     if mode == 'ByAge':
#         df65 = df[df['age'] >= 65]
#         df18 = df[(df['age'] >= 18) & (df['age'] < 65)]
#         df1 = df[(df['age'] > 0) & (df['age'] < 18)]
#
#         dic['cases_65'] = len(df65.loc[(df65['step'] == step) & (df65['state'] == 'mild')])
#         dic['admissions_65'] = len(
#             df65.loc[(df65['step'] == step) & ((df65['state'] == 'severe') | (df65['state'] == 'critical'))])
#         dic['deaths_65'] = len(df65.loc[(df65['step'] == step) & (df65['state'] == 'dead')])
#
#         dic['cases_18'] = len(df18.loc[(df18['step'] == step) & (df18['state'] == 'mild')])
#         dic['admissions_18'] = len(
#             df18.loc[(df18['step'] == step) & ((df18['state'] == 'severe') | (df18['state'] == 'critical'))])
#         dic['deaths_18'] = len(df18.loc[(df18['step'] == step) & (df18['state'] == 'dead')])
#
#         dic['cases_1'] = len(df1.loc[(df1['step'] == step) & (df1['state'] == 'mild')])
#         dic['admissions_1'] = len(
#             df1.loc[(df1['step'] == step) & ((df1['state'] == 'severe') | (df1['state'] == 'critical'))])
#         dic['deaths_1'] = len(df1.loc[(df1['step'] == step) & (df1['state'] == 'dead')])
#
#     elif mode == 'ByRace':
#         races = ['white', 'black', 'asian', 'other', 'two']
#         for race in races:
#             cases = len(df.loc[(df['race'] == race) & (df['step'] == step) & (df['state'] == 'mild')])
#             admissions = len(df.loc[(df['race'] == race) & (df['step'] == step) & ((df['state'] == 'severe') |
#                                                                                    (df['state'] == 'critical'))])
#             deaths = len(df.loc[(df['race'] == race) & (df['step'] == step) & (df['state'] == 'dead')])
#             dic['cases_' + race] = cases
#             dic['admissions_' + race] = admissions
#             dic['deaths_' + race] = deaths
#
#     elif mode == 'ByFPL':
#         groups = ['0-100', '100-150', '150-175', '175-200', '200-1800']
#         for group in groups:
#             temp = group.split('-')
#             lower = int(temp[0])
#             upper = int(temp[1])
#
#             cases = len(df.loc[((df['FPL'] > lower) & (df['FPL'] <= upper)) & (df['step'] == step) & (
#                     df['state'] == 'mild')])
#             admissions = len(df.loc[((df['FPL'] > lower) & (df['FPL'] <= upper)) & (df['step'] == step) & (
#                     (df['state'] == 'severe') | (df['state'] == 'critical'))])
#             deaths = len(df.loc[((df['FPL'] > lower) & (df['FPL'] <= upper)) & (df['step'] == step) & (
#                     df['state'] == 'dead')])
#
#             dic['cases_' + group] = cases
#             dic['admissions_' + group] = admissions
#             dic['deaths_' + group] = deaths
#
#     records.append(dic)
# print('Loading completed!')
# plotdf = pd.DataFrame(records)
# plotdf.to_csv(os.path.join(os.getcwd(),  'output', mode + '.csv'), index=False)
# # mode = "ByRace"
# code_dir = ''
plotdf = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), code_dir, 'SimulationEngine', 'output',   mode+ '.csv'))
plotdf = plotdf.sort_values(by='date')
if mode == 'ByAge':
    plot_age(plotdf)
elif mode == 'ByRace':
    plot_race(plotdf)
elif mode == 'ByFPL':
    plot_FPL(plotdf)