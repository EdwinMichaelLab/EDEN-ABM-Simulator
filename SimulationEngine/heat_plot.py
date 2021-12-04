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
import plotly.express as px

mapbox_access_token = 'pk.eyJ1IjoiaWhhc2htaSIsImEiOiJja3NwMTQ5MnMwMWZhMnVsY25tdzJvZHF4In0.WxPic21JaWmqPt5VAfshYg'
path = os.path.join(os.path.dirname(os.getcwd()),  'SimulationEngine', 'output', '2021-11-18')
print(path)
dlist = []
for root,dirs,files in os.walk(path):
    for file in files:
       if file.startswith("output_"):
           # no = file.split('_')[1].split('.')[0]
           d = pd.read_csv(os.path.join(root,file))
           dlist.append(d)

df = pd.concat(dlist)
df = df.sort_values(by=['step'])
steps = df['step'].unique().tolist()
startdate = datetime(2020, 3, 1)

fig = px.density_mapbox(df,
                        lat=df['y'],
                        lon=df['x'],
                        color=df['state'],
                        hover_name="pid",
                        animation_frame=df['step'],
                        zoom=12,
                        center=dict(lat=28.03711, lon=-82.46390),
                        mapbox_style='open-street-map'
                        )
fig.show()

py.offline.plot(fig, filename="Scatter-" + datetime.now().strftime("%Y-%m-%d") + ".html")


