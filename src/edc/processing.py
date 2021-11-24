import itertools
import pandas as pd
import numpy as np
import scipy
import scipy.spatial
from edc import utils 
from edc import optimisation 

df_trucks = pd.read_csv("../data/trucks.csv")
df_cities = pd.read_csv("../data/cities.csv")
df_routes = pd.read_csv("../data/routes_v2.csv")
df_routes["stops_list"] = df_routes.stops.apply(lambda row : row.split(' > '))
df_routes.drop(columns=['stops'],inplace=True)

def find_closest_warehouse(city,list_warehouse,return_index=False):
    dataframe_warehouse_cood = df_cities[df_cities.city.isin(list_warehouse)]
    distances = dataframe_warehouse_cood.apply(lambda row : utils.distance((row.lng,row.lat),utils.donnees_cities(city)),axis=1)
    index = distances.argmin()
    if return_index :
        return index
    else :
        return dataframe_warehouse_cood.iloc[index].city

def separate_in_warehouses(stops,dataframe_cities):
    dico_warehouse = {}
    for ville in stops :
        warehouse = dataframe_cities.loc[dataframe_cities.city == ville,'warehouse'].values[0]
        if warehouse in dico_warehouse.keys():
            dico_warehouse[warehouse].append(ville)
        else :
            dico_warehouse[warehouse] = [ville]
    return dico_warehouse

def try_scenario(df_cities_3,with_optim=False,df_routes=df_routes):
    df_routes['all_warehouses'] =  df_routes.stops_list.apply(lambda row : separate_in_warehouses(row,df_cities_3))
    df_routes['nb_warehouses'] =  df_routes.all_warehouses.apply(len)
    
    liste = []
    for i in range(len(df_routes.nb_warehouses)):
        liste.append(list(np.arange(df_routes.nb_warehouses.iloc[i])))

    merged = list(itertools.chain.from_iterable(liste))

    df_routes_separate = df_routes.loc[df_routes.index.repeat(df_routes.all_warehouses.apply(len))]
    df_routes_separate.index = np.arange(len(df_routes_separate))
    df_routes_separate = pd.concat( [df_routes_separate, pd.DataFrame(merged,columns=['index_order'])] , axis=1 , ignore_index=False)
    df_routes_separate['warehouse_f'] =  df_routes_separate.apply(lambda row : list(row.all_warehouses.keys())[row.index_order],axis=1)
    df_routes_separate['stops_list_f'] = df_routes_separate.apply(lambda row : row.all_warehouses[row.warehouse_f],axis=1)
    if with_optim :
        df_routes_separate['stops_list_ordonnee_f'] = df_routes_separate.apply(lambda row :optimisation.optimiser_trajectoire(utils.remove_consecutive_duplicate([utils.donnees_cities_with_name(row.warehouse_f)]+[utils.donnees_cities_with_name(city) for city in row.stops_list_f])),axis=1)
        df_routes_separate['total_distance_f'] = df_routes_separate.apply(lambda row : utils.total_distance_trip([row.warehouse_f]+row.stops_list_ordonnee_f), axis=1)
    else :
        df_routes_separate['total_distance_f'] = df_routes_separate.apply(lambda row : utils.total_distance_trip([row.warehouse_f]+row.stops_list_f), axis=1)
    
    return df_routes_separate

def filter_by_date_delay(dataframe,date,delay): 
    #création de la liste des delivery pour un jour de livraison précis
    return dataframe[dataframe["delivered_date"].isin([date - pd.Timedelta(days=i) for i in range(delay+1)])]

def processing_opti_rendement(df_orders_opt,warehouse_name,date,delay):

    df_filtered = df_orders_opt[df_orders_opt["from_warehouse"]==warehouse_name]
    df_filtered = filter_by_date_delay(df_filtered, date, delay)

    #Rajout une première ligne à 0 colis pour le warehouse
    date_str=date.strftime("%Y-%m-%d")
    lng_warehouse, lat_warehouse = utils.donnees_cities(warehouse_name)

    df_warehouse=pd.DataFrame(["","","0",warehouse_name,warehouse_name,date_str,date_str,0,0,lat_warehouse,lng_warehouse,lat_warehouse,lng_warehouse]).T
    df_warehouse.columns=df_filtered.columns
    df_filtered =pd.concat([df_warehouse,df_filtered])

    matrix_distance = scipy.spatial.distance.cdist(df_filtered[['lat_delivery','lng_delivery']],df_filtered[['lat_delivery','lng_delivery']], metric = utils.dist ).tolist()
    
    #Autres inputs
    demand=list(df_filtered["order_total_volume"])
    vehicle_capacities=[0.95*df_trucks["truck_volume"][0] for i in range (50)]
    num_vehicles=50
    depot=0

    return df_filtered,matrix_distance,demand,vehicle_capacities,num_vehicles,depot
    