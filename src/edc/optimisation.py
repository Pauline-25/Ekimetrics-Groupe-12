from edc import voyageur_de_commerce
from edc import utils

""""Voyageur de commerce"""

def optimiser_trajectoire(list_of_cities):
    """
    Execute le code de voyageur de commerce
    :param list_of_cities: lat,lng,name
    :return: - ancienne liste de ville
             - ancienne distance
             - nouvelle liste de ville
             - nouvelle distance
    """
    if len(list_of_cities)==1 :
        return [triplet[0] for triplet in list_of_cities]
    gc = voyageur_de_commerce.GestionnaireCircuit()

    for k in range(len(list_of_cities)):
        ville = voyageur_de_commerce.Ville(list_of_cities[k][1], list_of_cities[k][2], list_of_cities[k][0])
        gc.ajouterVille(ville)

    # on initialise la population avec 50 circuits
    pop = voyageur_de_commerce.Population(gc, 50, True)

    # On fait evoluer notre population sur 100 generations
    ga = voyageur_de_commerce.GA(gc)
    pop = ga.evoluerPopulation(pop)
    for i in range(0, 100):
        pop = ga.evoluerPopulation(pop)

    meilleurePopulation = pop.getFittest()
    list_of_new_cities = []
    for ville in meilleurePopulation.circuit:
        list_of_new_cities.append(ville.nom)

    # ordonner la nouvelle liste
    list_of_new_cities = utils.ordonner_une_liste(list_of_new_cities, list_of_cities[0][0])

    # on ajoute le trajet retour à l'ancienne distance
    return list_of_new_cities

def best_traject(row):
    list_of_cities_with_coord = [utils.donnees_cities_with_name(ville) for ville in row.stops_list]
    try :
        return optimiser_trajectoire(list_of_cities_with_coord)
    except :
        if len(row.stops_list) == 1 :
            return row.stops_list
        else :
            print(row.stops_list)
            raise ZeroDivisionError