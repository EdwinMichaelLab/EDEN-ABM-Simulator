import pandas as pd
import folium
from folium.plugins import HeatMapWithTime
from folium.plugins import HeatMap
from datetime import datetime, date, timedelta, time
import os
from datetime import datetime, date, timedelta, time
import branca.colormap

path = os.path.join(os.path.dirname(os.getcwd()), 'ABM-Simulator', 'SimulationEngine', 'output', '2021-11-23', '0', '33565')
dlist = []
for root,dirs,files in os.walk(path):
    for file in files:
        if file.startswith("output_"):
           no = file.split('_')[1].split('.')[0]
           d = pd.read_csv(os.path.join(root,file))
           d['chunk'] = no
           dlist.append(d)

df = pd.concat(dlist)
df = df.sort_values(by=['step'])
steps = df['step'].unique().tolist()
startdate = datetime(2020, 3, 1)

df["count"] = df.apply(lambda x:  0 if (x["state"] == "susceptible" or x["state"] == "asymptomatic"or x["state"] == "recovered"
                                        or x["state"] == "dead" or x["state"] == "vaccinated" or x["state"] == "boosted") else 1, axis=1)
df_list = []
for step in steps:
    df_list.append(df.loc[df.step == step, ['y', 'x', 'count']].groupby(['y', 'x']).sum().reset_index().values.tolist())

map = folium.Map(location=[28.03711,-82.46390], control_scale=True, zoom_start=10)
HeatMapWithTime(df_list, radius=7, gradient={.4: 'green', .65: 'orange', 1: 'red'}, index = steps,
                auto_play=True,
                min_opacity=0.75, max_opacity=1,
                use_local_extrema=True).add_to(map)
map.save("base_map3.html")
