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



if __name__ == '__main__':
    Total_time = time.time()
    ZIPS = ['33510', '33511', '33527', '33534', '33547', '33548', '33549', '33556', '33558', '33559', '33563', '33565',
            '33566', '33567', '33569', '33570', '33572', '33573', '33578', '33579', '33584', '33592', '33594', '33596',
            '33598', '33602', '33603', '33604', '33605', '33606', '33607', '33609', '33610', '33611', '33612', '33613',
            '33614', '33615', '33616', '33617', '33618', '33619', '33624', '33625', '33626', '33629', '33634', '33635',
            '33637', '33647', '33810']
    count=0
    for ZIP in ZIPS:
        #count+=1
        #if count>1:
        #    break

        print('Loading Started!')
        current_time = time.time()
        code_dir = "" #"ABM-Simulator"
        # code_dir = "SEIRCastSpatialABMSimulator"
        data = {}
        # Load households
        households = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), code_dir, 'SimulationEngine', 'input', 'ZIP',
                                              'households' + ZIP + '.csv'))

        # load people
        pop = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), code_dir, 'SimulationEngine', 'input', 'persons.csv'))
        delta_cases = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), code_dir,
                                               'SimulationEngine', 'input','cases_by_variants.csv'))

        #inject initial delta cases here
        initial_delta_cases = []
        delta_cases = delta_cases.sort_values(by='date')
        group = delta_cases.groupby('Date')
        for dt, grp in group:
            initial_delta_cases.append({'date': dt,
                                  'infected': pop.sample(n=len(grp))['pid'].values
                                  })
        data['initial_delta_cases'] = initial_delta_cases

        pop = pop.loc[pop['pid'].isin(households['occupant'])]
        # combine dataframes
        households = pd.merge(households, pop, left_on='occupant', right_on='pid')
        households = households.sample(n=1000)
        LG = gpd.read_file(os.path.join(os.path.dirname(os.getcwd()), code_dir, 'SimulationEngine', 'input', 'ZIP', ZIP + '.geojson'))
        LG = LG[['UID', 'type', 'x', 'y']]
        Locations = {}
        for index, row in LG.iterrows():
            Locations[row['UID']] = {'type': row['type'], 'x': row['x'], 'y': row['y']}

        data['Locations'] = Locations

        # load initial cases
        cases = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), code_dir, 'SimulationEngine', 'input', 'cases_by_zipcode.csv'))
        cases = cases[cases.zip==int(ZIP)]
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