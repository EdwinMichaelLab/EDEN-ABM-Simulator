import datetime
from dateutil.relativedelta import relativedelta
import datetime as dt
import pandas as pd
import os
import random
import threading

class Person():
    """Person Agent."""
    def __init__(self, pid, age, gender, race,  x, y, uid, loc_type, state, model):
        # threading.Thread.__init__(self)
        self.model = model
        # Agent parameters
        self.pid = pid
        self.age=age
        self.gender=gender
        self.race=race
        self.location = uid
        self.hid = uid   # a person always starts from home
        self.loc_type = loc_type
        self.x = x
        self.y = y
        self.hx = x
        self.hy = y

        self.moving = True
        #vaccination parameters
        self.vaccination_date = "none"
        self.vaccine_efficacy = 0.85

        #variants
        self.variant = 'none'
        self.state = state

        # Risk Probabilities
        self.recovery_rate = 0.2
        self.visit_count = 0

        self.infection_risk = 1.5
        self.default_infection_risk = 0.1
        # self.prob_asymptomatic = 0.5
        self.prob_asymptomatic = 0.75
        self.hospitalization_risk = 0.1624
        self.ICU_risk = 0.2527
        self.death_risk = 0.05

        # Phases
        self.exposed_to_presymptomatic = 6  # days
        self.presymptomatic_to_mild = 4
        self.mild_to_severe = 7
        self.severe_to_critical = 7
        self.critical_to_recovery = 8
        self.recovery_to_susceptible = 4
        self.asymptomatic_to_recovery = 4
        self.phase_count = 0
        code_dir = "" #'ABM-Simulator'
        # # load movements
        self.movements = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), code_dir, 'SimulationEngine', 'input', 'movements.csv'))
        self.movements.drop(self.movements[self.movements.start == self.movements.end].index, inplace=True)
        self.movements = self.movements[self.movements['age']==self.age]
        self.move_count = 0
        # # load lockdown
        self.lockdown = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), code_dir, 'SimulationEngine', 'input', 'lockdown.csv'))
        self.lockdown['date'] = pd.to_datetime(self.lockdown['date'], format='%Y-%m-%d').dt.date


    def print(self):
        print(self.pid, self.x, self.y, self.location, self.loc_type, self.state)

    def set_model(self, model):
        self.model = model

    def get_lockdown(self, current, type):
        if type=='house':
            return 1.0
        else:
            # current_date = datetime.datetime.strptime(current, '%Y-%m-%d').date()
            ld = self.lockdown.loc[(self.lockdown['date'] <= current), type]
            return ld.tail(1).values[0]

    def get_location(self, loc_type):
        if loc_type == 'house':
            return (self.hid, loc_type, self.hx, self.hy)
        elif loc_type == 'workplace':
            locs = list(self.model.workplaces.items())
            if len(locs) > 0:
                key, val = random.choice(locs)
                return (key, loc_type, val['x'], val['y'])
        elif loc_type == 'restaurant':
            locs = list(self.model.restaurants.items())
            if len(locs) > 0:
                key, val = random.choice(locs)
                return (key, loc_type, val['x'], val['y'])
        elif loc_type == 'worship':
            locs = list(self.model.worships.items())
            if len(locs) > 0:
                key, val = random.choice(locs)
                return (key, loc_type, val['x'], val['y'])
        elif loc_type == 'grocery':
            locs = list(self.model.grocerys.items())
            if len(locs) > 0:
                key, val = random.choice(locs)
                return (key, loc_type, val['x'], val['y'])
        elif loc_type == 'mall':
            locs = list(self.model.malls.items())
            if len(locs) > 0:
                key, val = random.choice(locs)
                return (key, loc_type, val['x'], val['y'])
        elif loc_type == 'school':
            locs = list(self.model.schools.items())
            if len(locs) > 0:
                key, val = random.choice(locs)
                return (key, loc_type, val['x'], val['y'])
        elif loc_type == 'outdoor':
            locs = list(self.model.outdoors.items())
            if len(locs) > 0:
                key, val = random.choice(locs)
                return (key, loc_type, val['x'], val['y'])
        elif loc_type == 'bank':
            locs = list(self.model.banks.items())
            if len(locs) > 0:
                key, val = random.choice(locs)
                return (key, loc_type, val['x'], val['y'])
        elif loc_type == 'hospital':
            locs = list(self.model.hospitals.items())
            if len(locs) > 0:
                key, val = random.choice(locs)
                return (key, loc_type, val['x'], val['y'])
        return None

    def get_route(self):
        mlist = []
        for row in self.movements.itertuples():
            start = getattr(row, 'start')
            end = getattr(row, 'end')
            start_loc = self.get_location(start)
            end_loc = self.get_location(end)
            # print(start_loc)
            if start_loc != None or end_loc != None:
                if start_loc!=end_loc:
                    mlist.append(start_loc)
                    mlist.append(end_loc)
        return mlist

    def randomTrue(self, prob):
        r = random.uniform(0, 1)
        if r < prob:
            return True
        else:
            return False

    def move(self, next):
        if next:
            if self.moving == True:
                if self.location != next[0]: # not at the same location
                    move_prob = self.get_lockdown(self.model.currentdate, next[1])
                    if self.randomTrue(move_prob):
                        #remove from current location
                        self.model.Locations[self.location].remove(self.pid)
                        self.location = next[0]
                        self.x = next[2]
                        self.y = next[3]
                        self.loc_type = next[1]
                        self.model.Locations[self.location].append(self.pid)
                        self.move_count+=1
                        # print(self.pid, 'moved to', self.loc_type)

    def get_infectionrisk(self, currentdate, variant):
        # risk = self.model.variants[self.model.variants.date==str(currentdate)]
        # if not risk.empty:
        #     if variant=="original":
        #         return risk['original'].values[0] + 0.01
        #     elif variant=="delta":
        #         return risk['delta'].values[0]
        # else:
        #     return self.default_infection_risk
        v = 0.1
        b = 0.125
        w = 0.1

        o = 0.3
        d = 0.5
        if self.state == "vaccinated":
            if variant=="original":
                return o - v
            elif variant=="delta":
                return d - v
        elif self.state == "boosted":
            if variant=="original":
                return o - b
            elif variant=="delta":
                return d - b
        elif self.state == "wanning":
            if variant=="original":
                return o - w
            elif variant=="delta":
                return d - w
        else:
            if variant=="original":
                return o
            elif variant=="delta":
                return d

    def maskwearing(self, currentdate):
        mw= self.model.variants[self.model.variants.date==str(currentdate)]
        if not mw.empty:
                val = mw['original'].values[0]
                return (1 - val)
        else:
            return 1

    def step(self):
        if self.state != "dead" and self.state != "severe" and self.state != "critical":
            routes = self.get_route()
            if routes != []:
                # for i, route in enumerate(routes):
                self.move(random.choice(routes))
        # print(self.pid, self.move_count)

        if (self.state == "susceptible") or (self.state == "vaccinated") or (self.state == "boosted") or (self.state == "wanning"):
            neighbors = self.model.Locations[self.location]
            for neighbor in neighbors:
                neighbor_person = self.model.persons[neighbor]
                if (neighbor_person.state == "presymptomatic"
                        or neighbor_person.state == "asymptomatic" or neighbor_person.state == "mild"
                        or neighbor_person.state == "severe" or neighbor_person.state == "critical"):
                            mask_wearing = self.randomTrue(self.maskwearing(self.model.currentdate))
                            if not mask_wearing:
                                inf_prob = self.randomTrue(self.get_infectionrisk(self.model.currentdate, neighbor_person.variant))
                                if inf_prob:
                                    self.state = "exposed"
                                    self.variant = neighbor_person.variant
                                    break

        elif self.state == "vaccinated":
            # process 1 doze
            # self.infection_risk = self.infection_risk * (1 - self.vaccine_efficacy)
            # administer booster after 21 days
            vacc_booster = datetime.datetime.strptime(self.vaccination_date, '%Y-%m-%d') + relativedelta(days=+21)
            if self.model.currentdate >= vacc_booster.date() and self.model.currentdate < vacc_booster.date() + relativedelta(days=+1):
                self.state = "boosted"
                # self.vaccine_efficacy = self.vaccine_efficacy + 0.1
                # self.infection_risk = self.infection_risk * (1 - self.vaccine_efficacy)
            # process vaccine wanning
            vacc_wanning = datetime.datetime.strptime(self.vaccination_date, '%Y-%m-%d') + relativedelta(months=+6)
            if self.model.currentdate >= vacc_wanning.date() and self.model.currentdate < vacc_wanning.date() + relativedelta(days=+1):
                self.state = "wanning"
                # print(self.pid, 'got wanning')
                # self.vaccine_efficacy = self.vaccine_efficacy * 0.9 # reduce efficacy to 10%
                # self.infection_risk = self.infection_risk * (1 - self.vaccine_efficacy)

        elif self.state == "exposed":
            self.phase_count += 1
            if (self.phase_count > self.exposed_to_presymptomatic):
                self.phase_count = 0
                if random.random() < self.prob_asymptomatic:
                    self.state = "asymptomatic"
                else:
                    self.state = "presymptomatic"

        elif self.state == "presymptomatic":
            self.phase_count += 1
            if (self.phase_count > self.presymptomatic_to_mild):
                self.state = "mild"
                self.phase_count = 0

        elif self.state == "mild":
            self.phase_count += 1
            if (self.phase_count > self.mild_to_severe):
                self.phase_count = 0
                if random.random() < self.hospitalization_risk:
                    self.state = "severe"
                    locs = list(self.model.hospitals.items())
                    if len(locs) > 0:
                        key, val = random.choice(locs)
                        self.move((key, 'hospital', val['x'], val['y']))
                    else:
                        self.move((self.hid, 'house', self.hx, self.hy))
                        self.moving = False
                else:
                    self.state = "recovered"

        elif self.state == "severe":
            self.phase_count += 1
            if (self.phase_count > self.severe_to_critical):
                self.phase_count = 0
                if random.random() < self.ICU_risk:
                    self.state = "critical"
                    # already in hospital
                else:
                    self.state = "recovered"

        elif self.state == "critical":
            self.phase_count += 1
            if (self.phase_count > self.critical_to_recovery):
                self.phase_count = 0
                if random.random() < self.death_risk:
                    self.state = "dead"
                    self.moving = False
                else:
                    self.state = "recovered"

        elif self.state == "asymptomatic":
            self.phase_count += 1
            if (self.phase_count > self.asymptomatic_to_recovery):
                self.phase_count = 0
                self.state = "recovered"

        elif self.state == "recovered":
            self.phase_count += 1
            if (self.phase_count > self.recovery_to_susceptible):
                self.phase_count = 0
                self.state = "susceptible"
                self.moving = True






