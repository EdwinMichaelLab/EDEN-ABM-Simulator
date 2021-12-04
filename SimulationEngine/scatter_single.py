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

path = os.path.join(os.path.dirname(os.getcwd()), 'ABM-Simulator', 'SimulationEngine', 'output', '2021-11-23', '3')
print(path)

step_from = 400 #609
step_to = 609 #609
dlist = []
for root,dirs,files in os.walk(path):
    for file in files:
       if file.startswith("output_"):
           no = int(file.split('_')[2].split('.')[0]) - 1
           if (no > step_from) and (no < step_to):
               d = pd.read_csv(os.path.join(root,file))
               d['chunk'] = no
               dlist.append(d)

df = pd.concat(dlist)
df = df.sort_values(by='step')
df['size']=4
df['color'] = df.apply(lambda x: 'blue' if x['state'] == 'susceptible' else ('orange' if x['state'] == 'exposed' else
                                                              ('purple' if x['state'] == 'asymptomatic' else
                                                               ('olive' if x['state'] == 'vaccinated' else
                                                                ('olive' if x['state'] == 'boosted' else
                                                                 ('green' if x['state'] == 'recovered' else
                                                                  ('black' if x['state'] == 'dead' else 'red')))))), axis=1)
#'blue', 'orange', 'purple', 'olive' , 'green' , 'black', 'red'
fig = px.scatter_mapbox(df, lat="y", lon="x",
                        color_discrete_sequence=['orange', 'red', 'red', 'darkred', 'black', 'blue',],
                        color= 'state',
                        size='size',
                        size_max=5,
                        animation_frame='step',
                        opacity=1,
                        zoom=10)
fig.update_layout(mapbox_style="open-street-map", title= "Hillsborough" + ' Location Graph', width=1000, height=800, legend=dict(x=0, y=0, orientation ="h"))
py.offline.plot(fig, filename= "Scatter.html")
fig.show()