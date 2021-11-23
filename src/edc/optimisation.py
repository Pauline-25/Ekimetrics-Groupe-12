from edc import voyageur_de_commerce
from edc import utils

def optimiser_trajectoire(list_of_cities):
    """
    Execute le code de voyageur de commerce
    :param list_of_cities: lat,lng,name
    :return: - ancienne liste de ville
             - ancienne distance
             - nouvelle liste de ville
             - nouvelle distance
    """
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
    # trajet_retour = utils.distance(list_of_cities[0], list_of_cities[-1])
    # ancienne_distance = df_routes.loc[1]['total_distance'] + trajet_retour

    # list of ancienne cities
    # list_of_only_old_cities = [list_of_cities[k][0] for k in range(len(list_of_cities))]

    # return list_of_only_old_cities, ancienne_distance, list_of_new_cities, pop.getFittest().getDistance()
    return list_of_new_cities