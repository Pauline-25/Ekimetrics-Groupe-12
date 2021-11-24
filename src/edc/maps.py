import folium
import pandas as pd

colors = ['blue','green','red','purple','orange']
df_warehouses = pd.read_csv("../data/warehouses.csv")
df_orders_lines = pd.read_csv("../data/intermediate_data/df_orders_lines.csv")
df_cities = pd.read_csv("../data/cities.csv")

dict_warehouse = {v: k for k, v in df_warehouses.to_dict()['warehouse_city'].items()}
min = df_orders_lines.order_total_volume.min()
max = df_orders_lines.order_total_volume.max()

def plotMarker(carte,point,color='blue',with_tooltip=True):
    tooltip = None
    if with_tooltip:
        tooltip = point.city
    folium.Marker(location=[point.lat, point.lng],
                  tooltip=tooltip,
                  icon=folium.Icon(color=color,icon='truck')
                  ).add_to(carte)

def plotDot(carte,point,colormap=None,color=None,with_tooltip = True):
    '''input: series that contains a numeric named latitude and a numeric named longitude
    this function creates a CircleMarker and adds it to your this_map'''
    if colormap is None :
        if color is None :
            cm = 'black'
        else :
            cm = color
    else :
        cm = colormap(point.order_total_volume)

    tooltip = str(point.city)
    if with_tooltip:
        tooltip = str(point.city) + " : volume of {}".format(int(point.order_total_volume))
    folium.CircleMarker(location=[point.lat, point.lng],
                        radius=2,
                        weight=5,
                        color=cm,
                        tooltip = tooltip
                        ).add_to(carte)

def plotLine(carte,order):
    point_warehouse = [order.lat_warehouse,order.lng_warehouse]
    point_delivery = [order.lat_delivery,order.lng_delivery]
    my_PolyLine = folium.PolyLine(locations=[point_warehouse,point_delivery],
                    weight= 0.1 + (order.order_total_volume - min) / (max-min) * 4,
                    color = colors[dict_warehouse[order.from_warehouse]]
                    )
    carte.add_child(my_PolyLine)

def plotTrajectoire(carte,cities,color='blue'):
    for i in range(len(cities)-1) :
        city_a = df_cities[df_cities.city == cities[i]] 
        city_b = df_cities[df_cities.city == cities[i+1]] 
        point_a = [float(city_a.lat),float(city_a.lng)]
        point_b = [float(city_b.lat),float(city_b.lng)]
        my_PolyLine = folium.PolyLine(locations=[point_a,point_b],
                        weight= 1,
                        color = color
                        )
        carte.add_child(my_PolyLine)                    