import pandas as pd
import os
import geopandas as gpd

class Locations():
    def __init__(self, ZIP):
        # load location graph
        code_dir = ""
        self.LG = gpd.read_file(os.path.join(os.path.dirname(os.getcwd()), code_dir, 'VE', 'GIS', 'ZIP', ZIP + '.geojson'))
        self.LG = self.LG[['UID', 'type', 'x', 'y']]
        self.Locations = {}
        for index, row in self.LG.iterrows():
            self.Locations[row['UID']] = {'type': row['type'], 'x': row['x'], 'y': row['y'], 'occupants': []}

    def print(self, uid):
        loc = self.Locations.get(uid)
        print(loc['type'], loc['x'], loc['y'], loc['occupants'])

    def get(self, uid):
        return self.Locations.get(uid)

    def get_occupants(self, uid):
        return self.Locations['occupants'].get(uid)

    def insert_occupant(self, uid, oid):
        self.Locations[uid]['occupants'].append(oid)

    def remove_occupant(self, uid, oid):
        self.Locations[uid]['occupants'].remove(oid)


if __name__ == '__main__':
    Locations = Locations('temp')
    Locations.print(71875)
    Locations.insert_occupant(71875, 1)
    Locations.insert_occupant(71875, 2)
    Locations.insert_occupant(71875, 3)
    Locations.insert_occupant(71875, 4)
    Locations.insert_occupant(71875, 5)
    Locations.print(71875)
    Locations.remove_occupant(71875, 5)
    Locations.print(71875)