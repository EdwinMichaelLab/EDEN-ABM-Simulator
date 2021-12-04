from multiprocessing import Process, Queue, Manager
import multiprocessing as mp
from datetime import datetime, date, timedelta, time
from dateutil.parser import parse
import random
from pandas.core.common import flatten
from shapely.geometry import Point, mapping, shape
import os
import geopandas as gpd
from geopandas import GeoDataFrame as gdf
from geopandas import points_from_xy
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import plotly.express as px
import  plotly as py
import plotly.graph_objects as go
import threading
import plotly
from multiprocessing import Manager, Pool, Lock
from SimulationEngine.Person import Person
from SimulationEngine.model import Model
from SimulationEngine.Loader import Loader
import itertools


def do_model(ZIP, index, chunk, data):
    model = Model(ZIP, index, chunk, data)

def assign_age_weight(age):
    if age >= 65:
        return 0.5
    elif age >= 30 & age < 65:
        return 0.3
    elif age >= 18 & age < 30:
        return 0.2
    else:
        return 0

if __name__ == '__main__':
    Total_time = time.time()

    print('Loading Started!')

    ZIP = 'All'

    current_time = time.time()
    code_dir = "ABM-Simulator"
    data = {}
    # Load households
    households = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), code_dir, 'SimulationEngine', 'input', 'households3.csv'))

    # load people
    pop = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), code_dir, 'SimulationEngine', 'input', 'persons.csv'))
    delta_cases = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), code_dir,
                                           'SimulationEngine', 'input','cases_by_variants.csv'))

    #inject initial delta cases here
    initial_delta_cases = []
    delta_cases = delta_cases.sort_values(by='Date')
    group = delta_cases.groupby('Date')
    for dt, grp in group:
        initial_delta_cases.append({'date': dt,
                              'infected': pop.sample(n=len(grp))['pid'].values
                              })
    data['initial_delta_cases'] = initial_delta_cases

    pop = pop.loc[pop['pid'].isin(households['occupant'])]
    # combine dataframes
    households = pd.merge(households, pop, left_on='occupant', right_on='pid')
    # households = households.sample(n=5000)
    LG = gpd.read_file(os.path.join(os.path.dirname(os.getcwd()), code_dir, 'SimulationEngine', 'input', 'LG3.geojson'))
    LG = LG[['UID', 'type', 'x', 'y']]
    Locations = {}
    for index, row in LG.iterrows():
        Locations[row['UID']] = {'type': row['type'], 'x': row['x'], 'y': row['y']}

    data['Locations'] = Locations

    # load initial cases
    cases = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), code_dir, 'SimulationEngine', 'input', 'cases.csv'))
    cases = cases.sort_values(by=['date'])
    initial_original_cases = []
    for index, row in cases.iterrows():
        initial_original_cases.append({ 'date': row['date'],
          'infected' : pop.sample(n=row['cases'])['pid'].values
        })

    data['initial_original_cases'] = initial_original_cases

    # load vaccination data
    vzip = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), code_dir, 'SimulationEngine', 'input', 'vaccine_by_zipcode.csv'))
    vzip = vzip[['date', ZIP]]
    weigths = pop.apply(lambda x: assign_age_weight(x['age']), axis=1)
    vaccinated = []
    for index, row in vzip.iterrows():
        vaccinated.append({'date': row['date'],
                                'persons': pop.sample(n=int(row[ZIP]), weights=weigths)['pid'].values})
    data['vaccinated'] = vaccinated

    # load variants data
    variants = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), code_dir, 'SimulationEngine', 'input','variants.csv'))
    data['variants'] = variants

    N = mp.cpu_count()  # define the number of processes
    chunk_size = int(len(households) / N)
    chunks = np.array_split(households, N)
    print('Job size: ', len(households), 'Chunk size', chunk_size)
    current_time = time.time()

    # Async pool
    pool = Pool(N)
    results = []  # if the function returnd a result we wanted
    for index, chunk in enumerate(chunks):
        result = pool.apply_async(do_model, (ZIP, index, chunk, data))
        results.append(result)
    for result in results:
        result = result.get()
    pool.close()
    pool.join()

    print('Simulation stopped!')
    print('Total time:', (time.time() - Total_time) / 60)