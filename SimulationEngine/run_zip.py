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


def do_model(ZIP):
    model = Model(ZIP)

if __name__ == '__main__':
    Total_time = time.time()
    # ZIPS = ['33510', '33511', '33527', '33534', '33547', '33548', '33549', '33556', '33558', '33559', '33563', '33565',
    #         '33566', '33567', '33569', '33570', '33572', '33573', '33578', '33579', '33584', '33592', '33594', '33596',
    #         '33598', '33602', '33603', '33604', '33605', '33606', '33607', '33609', '33610', '33611', '33612', '33613',
    #         '33614', '33615', '33616', '33617', '33618', '33619', '33624', '33625', '33626', '33629', '33634', '33635',
    #         '33637', '33647']

    ZIPS = ['33613']

    print('Loading Started!')
    code_dir = "" #"ABM-Simulator"
    # # Async pool
    pool = mp.Pool(processes=len(ZIPS))
    pool.map(do_model, ZIPS)
    pool.close()
    pool.join()
    print('Simulation stopped!')
    print('Total time:', (time.time() - Total_time) / 60)