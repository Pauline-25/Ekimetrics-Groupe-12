import numpy as np
import pandas as pd
from itertools import groupby
from geopy import distance 

try :
    df_cities = pd.read_csv("../data/cities.csv")
except :
    df_cities = pd.read_csv("./data/cities.csv")

def donnees_cities(name_city):
    """
    Fontion qui va recupérer les données de lattitude et longitude
    """
    donnees_city = df_cities[df_cities.city == name_city]
    try :
        lat, long = float(donnees_city['lat'].iloc[0]), float(donnees_city['lng'].iloc[0])
    except :
        print(name_city)
        print(donnees_city)
        lat, long = float(donnees_city['lat']), float(donnees_city['lng'])
    return long, lat

def donnees_cities_with_name(name_city):
    return [name_city] + list(donnees_cities(name_city))

def dist(x,y):
    return int(distance.distance(x,y).km)

def ordonner_une_liste(list, first_element):
    index = list.index(first_element)
    new_list = []
    for k in range(len(list)):
        new_list.append(list[(index+k)%len(list)])
    return new_list

def total_distance_trip(cities):
    dist = 0
    if len(cities) > 1 :
        for i in range(len(cities)):            
            dist += distance.distance(donnees_cities(cities[i]) , donnees_cities(cities[(i+1) % len(cities)])).km
    return dist

def remove_consecutive_duplicate(liste):
    return [x[0] for x in groupby(liste)]

def str_to_list(string):
    if type(string) is float:
        return np.nan
    else :
        list_string =  string.split(",")
        for i in range(len(list_string)):
            list_string[i] = [list_string[i].replace('[','').replace(']','').replace("'",'').replace(" ",'')]
        return list_string