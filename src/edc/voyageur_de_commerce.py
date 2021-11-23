import pandas as pd
import random
import math

class Ville:
    def __init__(self, lon, lat, nom):
        self.lon = lon
        self.lat = lat
        self.nom = nom

    def distance(self, ville):
        distanceX = (ville.lon-self.lon)*40000*math.cos((self.lat+ville.lat)*math.pi/360)/360
        distanceY = (self.lat-ville.lat)*40000/360
        distance = math.sqrt( (distanceX*distanceX) + (distanceY*distanceY) )
        return distance


class GestionnaireCircuit:

    def __init__(self):
        self.villesDestinations = [] 

    def ajouterVille(self, ville):
        self.villesDestinations.append(ville)

    def getVille(self, index):
        return self.villesDestinations[index]

    def nombreVilles(self):
        return len(self.villesDestinations)


class Circuit:
    def __init__(self, gestionnaireCircuit, circuit=None):
        self.gestionnaireCircuit = gestionnaireCircuit
        self.circuit = []
        self.fitness = 0.0
        self.distance = 0
        if circuit is not None:
            self.circuit = circuit
        else:
            for i in range(0, self.gestionnaireCircuit.nombreVilles()):
                self.circuit.append(None)

    def __len__(self):
        return len(self.circuit)

    def __getitem__(self, index):
        return self.circuit[index]

    def __setitem__(self, key, value):
        self.circuit[key] = value

    def genererIndividu(self):
        for indiceVille in range(0, self.gestionnaireCircuit.nombreVilles()):
            self.setVille(indiceVille, self.gestionnaireCircuit.getVille(indiceVille))
        random.shuffle(self.circuit)

    def getVille(self, circuitPosition):
        return self.circuit[circuitPosition]

    def setVille(self, circuitPosition, ville):
        self.circuit[circuitPosition] = ville
        self.fitness = 0.0
        self.distance = 0

    def getFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.getDistance())
        return self.fitness

    def getDistance(self):
        if self.distance == 0:
            circuitDistance = 0
            for indiceVille in range(0, self.tailleCircuit()):
                villeOrigine = self.getVille(indiceVille)
                villeArrivee = None
                if indiceVille + 1 < self.tailleCircuit():
                    villeArrivee = self.getVille(indiceVille + 1)
                else:
                    villeArrivee = self.getVille(0)
                circuitDistance += villeOrigine.distance(villeArrivee)
            self.distance = circuitDistance
        return self.distance

    def tailleCircuit(self):
        return len(self.circuit)

    def contientVille(self, ville):
        return ville in self.circuit


class Population:
    def __init__(self, gestionnaireCircuit, taillePopulation, init):
        self.circuits = []
        for i in range(0, taillePopulation):
            self.circuits.append(None)

        if init:
            for i in range(0, taillePopulation):
                nouveauCircuit = Circuit(gestionnaireCircuit)
                nouveauCircuit.genererIndividu()
                self.sauvegarderCircuit(i, nouveauCircuit)

    def __setitem__(self, key, value):
        self.circuits[key] = value

    def __getitem__(self, index):
        return self.circuits[index]

    def sauvegarderCircuit(self, index, circuit):
        self.circuits[index] = circuit

    def getCircuit(self, index):
        return self.circuits[index]

    def getFittest(self):
        fittest = self.circuits[0]
        for i in range(0, self.taillePopulation()):
            if fittest.getFitness() <= self.getCircuit(i).getFitness():
                fittest = self.getCircuit(i)
        return fittest

    def taillePopulation(self):
        return len(self.circuits)


class GA:
    def __init__(self, gestionnaireCircuit):
        self.gestionnaireCircuit = gestionnaireCircuit
        self.tauxMutation = 0.015
        self.tailleTournoi = 5
        self.elitisme = True

    def evoluerPopulation(self, pop):
        nouvellePopulation = Population(self.gestionnaireCircuit, pop.taillePopulation(), False)
        elitismeOffset = 0
        if self.elitisme:
            nouvellePopulation.sauvegarderCircuit(0, pop.getFittest())
            elitismeOffset = 1

        for i in range(elitismeOffset, nouvellePopulation.taillePopulation()):
            parent1 = self.selectionTournoi(pop)
            parent2 = self.selectionTournoi(pop)
            enfant = self.crossover(parent1, parent2)
            nouvellePopulation.sauvegarderCircuit(i, enfant)

        for i in range(elitismeOffset, nouvellePopulation.taillePopulation()):
            self.muter(nouvellePopulation.getCircuit(i))

        return nouvellePopulation

    def crossover(self, parent1, parent2):
        enfant = Circuit(self.gestionnaireCircuit)

        startPos = int(random.random() * parent1.tailleCircuit())
        endPos = int(random.random() * parent1.tailleCircuit())

        for i in range(0, enfant.tailleCircuit()):
            if startPos < endPos and i > startPos and i < endPos:
                enfant.setVille(i, parent1.getVille(i))
            elif startPos > endPos:
                if not (i < startPos and i > endPos):
                    enfant.setVille(i, parent1.getVille(i))

        for i in range(0, parent2.tailleCircuit()):
            if not enfant.contientVille(parent2.getVille(i)):
                for ii in range(0, enfant.tailleCircuit()):
                    if enfant.getVille(ii) == None:
                        enfant.setVille(ii, parent2.getVille(i))
                        break

        return enfant

    def muter(self, circuit):
        for circuitPos1 in range(0, circuit.tailleCircuit()):
            if random.random() < self.tauxMutation:
                circuitPos2 = int(circuit.tailleCircuit() * random.random())

                ville1 = circuit.getVille(circuitPos1)
                ville2 = circuit.getVille(circuitPos2)

                circuit.setVille(circuitPos2, ville1)
                circuit.setVille(circuitPos1, ville2)

    def selectionTournoi(self, pop):
        tournoi = Population(self.gestionnaireCircuit, self.tailleTournoi, False)
        for i in range(0, self.tailleTournoi):
            randomId = int(random.random() * pop.taillePopulation())
            tournoi.sauvegarderCircuit(i, pop.getCircuit(randomId))
        fittest = tournoi.getFittest()
        return fittest
