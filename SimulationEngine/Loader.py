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
from SimulationEngine.Person import Person
import matplotlib.pyplot as plt
import plotly.express as px
import  plotly as py
import plotly.graph_objects as go
import threading
import plotly
import multiprocessing as mp
from multiprocessing import Manager, Pool, Lock
import distutils.dir_util

class Loader():
    def __init__(self, ZIP, i, chunk, persons, lock):
        my_persons = {}
        houses = chunk["hid"].unique()

        my_persons = []
        for house in houses:
            occupants = chunk.loc[chunk.hid == house]
            for row in occupants.itertuples():
                occupant = getattr(row, "occupant")
                pid = getattr(row, "pid")
                age = getattr(row, "age")
                gender = getattr(row, "gender")
                race = getattr(row, "race")
                housex = getattr(row, "x")
                housey = getattr(row, "y")

                this_person = Person(pid, age, gender, race, housex, housey, int(house), "house", "susceptible")
                my_persons.append(this_person)

        with lock:
            persons.extend(my_persons)
        print("Loader", i, "has loaded", "Zip Code:", ZIP, "Population:", len(my_persons))