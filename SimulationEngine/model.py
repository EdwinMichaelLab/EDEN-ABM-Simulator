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
import asyncio
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class Model():
    def __init__(self, ZIP):
        self.ZIP = ZIP
        self.startdate = date(2020, 3, 1)
        self.currentdate = self.startdate
        self.enddate = date(2021, 10, 31)

        self.step = 0
        self.Lock_down = True
        self.output = []
        self.SEIR = []

        self.move_count = 0
        self.part = 0
        self.current_time = datetime.now()
        code_dir = ""
        # Load households
        self.households = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), code_dir, 'SimulationEngine', 'input', 'ZIP',
                         'households' + ZIP + '.csv'))
        pop = pd.read_csv(
            os.path.join(os.path.dirname(os.getcwd()), code_dir, 'SimulationEngine', 'input', 'persons.csv'))
        # combine dataframes
        self.households = pd.merge(self.households, pop, left_on='occupant', right_on='pid')
        # n = 2000
        # self.percent = 1
        # self.households = self.households.sample(frac=1)
        pop = pop.loc[pop['pid'].isin(self.households['occupant'])]
        LG = gpd.read_file(
            os.path.join(os.path.dirname(os.getcwd()), code_dir, 'SimulationEngine', 'input', 'ZIP', ZIP + '.geojson'))
        LG = LG[['UID', 'type', 'x', 'y']]


        self.Locations = {}
        Locs = LG['UID'].unique().tolist()
        for loc in Locs:
            self.Locations[loc] = []

        self.workplaces = {}
        LLG = LG.loc[LG['type'] == 'workplace']
        for index, row in LLG.iterrows():
            self.workplaces[row['UID']] = {'x': row['x'], 'y': row['y']}

        self.restaurants = {}
        LLG = LG.loc[LG['type'] == 'restaurant']
        for index, row in LLG.iterrows():
            self.restaurants[row['UID']] = {'x': row['x'], 'y': row['y']}

        self.worships = {}
        LLG = LG.loc[LG['type'] == 'worship']
        for index, row in LLG.iterrows():
            self.worships[row['UID']] = {'x': row['x'], 'y': row['y']}

        self.grocerys = {}
        LLG = LG.loc[LG['type'] == 'grocery']
        for index, row in LLG.iterrows():
            self.grocerys[row['UID']] = {'x': row['x'], 'y': row['y']}

        self.malls = {}
        LLG = LG.loc[LG['type'] == 'mall']
        for index, row in LLG.iterrows():
            self.malls[row['UID']] = {'x': row['x'], 'y': row['y']}

        self.schools = {}
        LLG = LG.loc[LG['type'] == 'school']
        for index, row in LLG.iterrows():
            self.schools[row['UID']] = {'x': row['x'], 'y': row['y']}

        self.outdoors = {}
        LLG = LG.loc[LG['type'] == 'outdoor']
        for index, row in LLG.iterrows():
            self.outdoors[row['UID']] = {'x': row['x'], 'y': row['y']}

        self.banks = {}
        LLG = LG.loc[LG['type'] == 'bank']
        for index, row in LLG.iterrows():
            self.banks[row['UID']] = {'x': row['x'], 'y': row['y']}

        self.hospitals = {}
        LLG = LG.loc[LG['type'] == 'hospital']
        for index, row in LLG.iterrows():
            self.hospitals[row['UID']] = {'x': row['x'], 'y': row['y']}

        # load initial cases
        self.initial_cases = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), code_dir, 'SimulationEngine', 'input', 'initial_cases_byzip.csv'))
        self.initial_cases = self.initial_cases[self.initial_cases.zip == int(ZIP)]
        self.initial_cases = self.initial_cases.sort_values(by=['date'])

        # load vaccination data
        vzip = pd.read_csv(
            os.path.join(os.path.dirname(os.getcwd()), code_dir, 'SimulationEngine', 'input', 'vaccine_by_zipcode.csv'))
        vzip = vzip[['date', ZIP]]
        weigths = pop.apply(lambda x: self.assign_age_weight(x['age']), axis=1)
        self.vaccinated  = []
        for index, row in vzip.iterrows():
            self.vaccinated.append({'date': row['date'],
                               'persons': pop.sample(n=int(row[ZIP]), weights=weigths)['pid'].values})

        # load variants data
        self.variants = pd.read_csv(
            os.path.join(os.path.dirname(os.getcwd()), code_dir, 'SimulationEngine', 'input', 'variants.csv'))

        self.persons = {}
        self.houses = self.households["hid"].unique()
        for house in self.houses:
            occupants = self.households.loc[self.households.hid == house]
            for row in occupants.itertuples():
                occupant = getattr(row, "occupant")
                pid = getattr(row, "pid")
                age = getattr(row, "age")
                gender = getattr(row, "gender")
                race = getattr(row, "race")
                housex = getattr(row, "x")
                housey = getattr(row, "y")
                person = Person(pid, age, gender, race, housex, housey, int(house), "house", "susceptible", self)
                self.persons[pid] = person
                self.Locations[int(house)].append(pid) #add occupants to the building

        print("Model", "has loaded", "Zip Code:", ZIP, "Population:", len(self.persons), self.get_time())
        self.running = True

        #move some people
        # location_types = ['house', 'workplace','restaurant', 'worship','grocery','mall','school','outdoor','bank','hospital']
        # ps = pop['pid'].sample(n=300).tolist()
        # for p in ps:
        #     person = self.persons[p]
        #     gl = list(self.grocerys.keys())
        #     if len(gl)>0:
        #         grocery_id = random.choice(gl)
        #         grocery = self.grocerys[grocery_id]
        #         person.move((grocery_id, 'grocery', grocery['x'], grocery['y']))

        while self.running:
            self.doTimeStep()

    def assign_age_weight(self, age):
        if age >= 65:
            return 0.5
        elif age >= 30 & age < 65:
            return 0.3
        elif age >= 18 & age < 30:
            return 0.2
        else:
            return 0

    def get_rand_person(self):
        pl = list(self.persons.keys())
        for i in range(len(pl)):
            pid = random.choice(pl)
            person = self.persons[pid]
            if person.loc_type!='house':
                return person
        return None

    def get_time(self):
        t = datetime.now()
        d = datetime.now() - self.current_time
        self.current_time = datetime.now()
        return '[' + str(d.seconds) + 'sec' ' ' + str(t).split(' ')[1].split('.')[0] + ']'

    def do_vaccinations(self):
        vac_dic = [item for item in self.vaccinated if item['date'] == str(self.currentdate)]
        if vac_dic:  # meaning there is one or more initial cases on this date
            vac_list = vac_dic[0]['persons']
            for vac in vac_list:
                person = self.persons[vac]
                if person:
                    person.state = 'vaccinated'
                    person.vaccination_date = str(self.currentdate)
                    # self.set_state(person.pid, person.state)

    def do_initialinfections(self):
        initial_infections = self.initial_cases.loc[(self.initial_cases['date'] == str(self.currentdate))]
        if not initial_infections.empty:
            original_infections = int(initial_infections['original'].values[0] * 0.5)
            delta_infections = int(initial_infections['delta'].values[0] * 0.5)
            # print(self.ZIP, original_infections, delta_infections)
            if self.currentdate <= date(2020, 3, 30):
                for i in range(original_infections):
                    person = self.get_rand_person()
                    if person:
                        if person.state != 'vaccinated':
                            person.state = 'presymptomatic'
                            person.variant = 'original'
                            self.persons[person.pid] = person

            if (self.currentdate >= date(2021, 7, 1)) and (self.currentdate <= date(2021, 9, 1)):
                for j in range(delta_infections):
                    person = self.get_rand_person()
                    if person:
                        if person.state != 'vaccinated':
                            person.state = 'presymptomatic'
                            person.variant = 'delta'
                            self.persons[person.pid] = person

    def doTimeStep(self):
        self.currentdate = self.startdate + timedelta(days=self.step)
        self.do_vaccinations()
        self.do_initialinfections()

        for key, person in self.persons.items():
            person.step()

        self.update_output()
        self.step += 1

        print(self.ZIP, 'has completed step: ', self.step, '---', self.currentdate, '|', 'Time', self.get_time())
        d = self.enddate - self.startdate
        self.save()

        if self.currentdate >= self.enddate:
            self.running = False

    def save(self):
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d")
        outdir = os.path.join(os.getcwd(), 'output', dt_string, 'run1', self.ZIP, )
        distutils.dir_util.mkpath(outdir)
        if self.output!=[]:
            df = pd.DataFrame(self.output)
            file1 = os.path.join(outdir, 'output_' + self.ZIP + '_' + str(self.step) + '.csv')
            df.to_csv(file1, index=False)
            self.output = []

        sdf = pd.DataFrame(self.SEIR)
        file2 = os.path.join(outdir, 'SEIR_' + self.ZIP + '.csv')
        sdf.to_csv(file2, index=False)


    def update_output(self):
        seir = {'step': self.step, 'susceptible': 0, 'vaccinated': 0, 'boosted':0, 'wanning':0, 'exposed': 0, 'asymptomatic': 0, 'presymptomatic': 0, 'mild': 0,
         'severe': 0, 'critical': 0, 'recovered': 0, 'dead': 0}

        for key, person in self.persons.items():
            seir[person.state]+=1
            if (person.state != "susceptible") and (person.state != "vaccinated") and \
                    (person.state != "asymptomatic") and (person.state != "recovered"):
                        result = {'step': self.step, 'pid': person.pid, 'x': person.x, 'y': person.y, 'location': person.location,
                                  'ZIP': person.model.ZIP, 'type': person.loc_type, 'state': person.state}
                        self.output.append(result)

        self.SEIR.append(seir)

    def get_location_by_type(self, type):
        temp = []
        for uid, values in self.Locations.items():
            if values['type']==type:
                temp.append((uid, values))
        if temp!=[]:
            r = random.randint(0,len(temp)-1)
            return temp[r]
        else:
            None

    def get_location_by_id(self, uid):
        for id, values in self.Locations.items():
            if id==uid:
                return (uid, values)
