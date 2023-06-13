import os
import pickle
from data import Data


# Looks for saveData.txt file and deserialize and returs the object Data.
def initialization_data():
    data = Data()
    dir = os.path.abspath(os.getcwd()) + "\saveData.txt"
    if os.path.exists(dir):
        with open(dir, "br") as f:
            data = pickle.load(f)
    return data


# Expects a Path var. Looks for the path and reads the file.
# Extracts and return the Vertices and Edges in a list
def read_map_var(path: str):
    mapV = []
    if os.path.exists(path):
        with open(path, "r") as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace(" ", "")
                if mapV == []:
                    mapV.append(line[3:-2].split(","))
                else:
                    mapV.append(line[4:-2].split(">,<"))
    for i in range(0, len(mapV[1])):
        mapV[1][i] = mapV[1][i].split(",")
    return mapV


# Creates file or overwrites data and serializes the Data Object
def saves_data(data):
    dir = os.path.abspath(os.getcwd()) + "\saveData.txt"
    file = open(dir, 'bw')
    pickle.dump(data, file)
    file.close()
