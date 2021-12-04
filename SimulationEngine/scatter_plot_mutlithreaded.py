import os
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import json
import numpy as np
import timeit
from datetime import datetime
from scipy.interpolate import griddata
from numpy import linspace
import plotly.express as px
from shapely.geometry import Polygon, MultiPolygon
import geopandas as gpd
from datetime import datetime
import matplotlib.pyplot as plt
# import geojsoncontour
from plotly.offline import iplot
# Set global theme
import plotly.figure_factory as ff
import plotly.graph_objects as go
import  plotly as py
from datetime import datetime, date, timedelta, time

import queue
import threading
import time

# Class
class MultiThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        # print("Starting job:", self.name)
        self.process_queue()
        print("Completed job", self.name)

    # Process thr queue
    def process_queue(self):
        while True:
            try:
                value = my_queue.get(block=False)
            except queue.Empty:
                return
            else:
                self.do_job(value)
                time.sleep(1)

    def do_job(self, step):
        sdate = str((startdate + timedelta(days=step)).date())
        frame = {"data": [], "name": step}
        trace = dict(
            lat=df.loc[df['step'] <= step, 'y'],
            lon=df.loc[df['step'] <= step, 'x'],
            type="scattermapbox",
            mode='markers',
            marker=dict(
                size=6,
                color=list(map(lambda x: 'blue' if x == 'susceptible' else ('orange' if x == 'exposed' else (
                    'purple' if x == 'asymptomatic' else ('olive' if x == 'vaccinated' else (
                        'olive' if x == 'boosted' else (
                            'green' if x == 'recovered' else ('black' if x == 'dead' else 'red')))))),
                               df.loc[df['step'] <= step, 'state'].values)),
                opacity=1,
                colorscale="jet"),
            text=df.loc[df['step'] <= step, 'state'].values,
        )
        frame["data"].append(trace)
        frames.append(frame)
        sdate = str((startdate + timedelta(days=step)).date())
        slider_step = {"args": [
            [step],
            {"frame": {"duration": 100, "redraw": True},
             "mode": "immediate",
             "transition": {"duration": 100}}
        ],
            "label": step,
            "method": "animate"}
        sliders_dict["steps"].append(slider_step)

path = os.path.join(os.path.dirname(os.getcwd()),  'SimulationEngine', 'output', '2021-11-04')
print(path)
dlist = []
for root,dirs,files in os.walk(path):
    for file in files:
       if file.endswith(".csv"):
           no = file.split('_')[1].split('.')[0]
           d = pd.read_csv(os.path.join(root,file))
           d['chunk'] = no
           dlist.append(d)

df = pd.concat(dlist)
df = df.sort_values(by=['step'])
steps = df['step'].unique().tolist()
startdate = datetime(2020, 3, 1)

data = []
trace0 = dict(
    lat=df.loc[df['step']==25,'y'],
    lon=df.loc[df['step']==25,'x'],
    type="scattermapbox",
    mode='markers',
    marker=dict(
        size=6,
        color= list(map(lambda x:  'blue' if x == 'susceptible' else ('orange' if x == 'exposed' else ('purple' if x == 'asymptomatic' else ('olive' if x == 'vaccinated' else ('olive' if x == 'boosted' else ('green' if x == 'recovered' else ('black' if x == 'dead' else 'red')))))), df.loc[df['step']==25,'state'].values)),
        opacity=1,
        colorscale="jet"),
    text=df.loc[df['step']==25,'state'].values,
)
data = [trace0]

sliders_dict = {
    'active': 0,
    'yanchor': 'top',
    'xanchor': 'left',
    'currentvalue': {
        'font': {'size': 20},
        'prefix': 'Day:',
        'visible': True,
        'xanchor': 'right'
    },
    'transition': {'duration': 300, 'easing': 'cubic-in-out'},
    'pad': {'b': 10, 't': 50},
    'len': 0.9,
    'x': 0.1,
    'y': 0,
    'steps': []
}

frames = []
threads = []
my_queue = queue.Queue()
for step in steps:
    my_queue.put(step)
    thread = MultiThread(str(step))
    threads.append(thread)
    if step>100:
        break
print(my_queue.qsize())
for thread in threads:
    thread.start()


for thread in threads:
    thread.join()

print('Loading completed!')
layout = go.Layout(
    title="Hillsborough COVID-19 Transmission",
    title_x=0.4,
    height=1200,
    # top, bottom, left and right margins
    margin=dict(t=80, b=0, l=0, r=0),
    font=dict(color='dark grey', size=18),
    mapbox=dict(
        center=dict(lat=28.03711, lon=-82.46390),
        # default level of zoom
        zoom=12,
        # default map style
        style="open-street-map"
    )
)
layout["sliders"] = [sliders_dict]
layout['updatemenus'] = [
    {
        'buttons': [
            {
                'args': [None, {'frame': {'duration': 100, 'redraw': True},
                         'fromcurrent': True, 'transition': {'duration': 100, 'easing': 'quadratic-in-out'}}],
                'label': 'Play',
                'method': 'animate'
            },
            {
                'args': [[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate',
                'transition': {'duration': 0}}],
                'label': 'Pause',
                'method': 'animate'
            }
        ],
        'direction': 'left',
        'pad': {'r': 10, 't': 87},
        'showactive': False,
        'type': 'buttons',
        'x': 0.1,
        'xanchor': 'right',
        'y': 0,
        'yanchor': 'top'
    }
]
figure = dict(
    data=data,
    layout=layout,
    frames = frames
)

py.offline.plot(figure, filename="Scatter-" + datetime.now().strftime("%Y-%m-%d") + ".html")


