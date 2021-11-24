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
        print(donnees_city)
        lat, long = float(donnees_city['lat']), float(donnees_city['lng'])
    return long, lat

def donnees_cities_with_name(name_city):
    return [name_city] + list(donnees_cities(name_city))

def dist(x,y):
    return int(distance.distance(x,y).km)

# def distance(tuple_city1,tuple_city2):
#     """
#     Fonction qui renvoie la distance à vol d'oiseau entre deux villes en fonction des couples (long,lat)
#     """
#     if tuple_city1 == tuple_city2 :
#         return 0
#     long_city1, lat_city1 = np.pi*tuple_city1[0]/180, np.pi*tuple_city1[1]/180
#     long_city2, lat_city2 = np.pi*tuple_city2[0]/180, np.pi*tuple_city2[1]/180
#     return 6371*np.arccos(np.sin(lat_city1)*np.sin(lat_city2)+np.cos(lat_city1)*np.cos(lat_city2)*np.cos(long_city1-long_city2))

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
            dist += distance(donnees_cities(cities[i]) , donnees_cities(cities[(i+1) % len(cities)]))
    return dist

def remove_consecutive_duplicate(liste):
    return [x[0] for x in groupby(liste)]