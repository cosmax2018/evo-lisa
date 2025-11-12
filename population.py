
# population.py : simple GA v.2 written in Python (slow version)

#    (c) Copyright 2020-25 by ....@_°° Lumachina SW
#    Massimiliano Cosmelli (massimiliano.cosmelli@gmail.com)

import random, time, itertools

from individual import Individual

class Population():
    # classe di inizializzazione o costruttore
    def __init__(self,populationSize,tournamentSize,mutationRate,alphabet,chromosomeLength,objectiveFunction,sharedData = None):
        self.populationSize     = populationSize    # dimensione della popolazione
        self.tournamentSize     = tournamentSize    # dimensione della selezione
        self.mutationRate       = mutationRate      # rateo di mutazione
        self.alphabet           = alphabet          # alfabeto su cui si basano i cromosomi
        self.chromosomeLength   = chromosomeLength  # lunghezza dei cromosomi
        self.objectiveFunction  = objectiveFunction # la funzione obiettivo
        
        self.individuals = []                       # la popolazione di individui
        
        self.randomize()
        for i in range(populationSize):
            self.individuals.append(Individual(alphabet,chromosomeLength,objectiveFunction)) # istanzia un nuovo individuo        
            
    def randomize(self):            random.seed(time.time())
    
    def getIndividuals(self):       return self.individuals     # restituisce gli individui della popolazione
        
    def getIndividual(self,i):      return self.individuals[i]  # restituisce l'individuo i-esimo
    
    def setIndividual(self,i,v):    self.individuals[i] = v     # setta l'individuo i-esimo
    
    def rndPopulation(self):
        # genera una popolazione casuale di individui dal cromosoma generato a caso
        for individual in self.individuals:
            individual.rndIndividual()

    def evaluatePopulation(self):
        # valuta la popolazione di individui
        for individual in self.individuals:
            individual.setFitness()
            
    def sortPopulation(self):
        # ordina la popolazione in base alla fitness
        for i,j in itertools.product(range(self.populationSize),range(self.populationSize)):
            if self.individuals[i].getFitness() > self.individuals[j].getFitness():
                self.individuals[i],self.individuals[j] = self.individuals[j],self.individuals[i]
                
    def mutatePopulation(self):
        # genera delle mutazioni casuali in alcuni individui della popolazione
        for individual in self.individuals:
            if random.random() < self.mutationRate:
                individual.mutateIndividual()
                
    def evolvePopulation(self):
        # fa un passo evolutivo incrociando i migliori individui a 2 a 2
        for i in range(0,self.tournamentSize,2):
            child1,child2 = self.individuals[i].crossoverIndividuals(self.individuals[i+1])
            self.individuals[self.populationSize-i-1].setIndividuals(child1)
            self.individuals[self.populationSize-i-2].setIndividuals(child2)
            
    def replaceWhorst(self,threshold):
        # rimpiazza i peggiori individui della popolazione con altrettanti individui generati a caso
        for individual in self.individuals:
            if individual.getFitness() < threshold:
                individual.rndIndividual()

    def getWorstFitness(self):
        # la fitness del peggior individuo della popolazione
        return self.individuals[-1].getFitness()
        
    def getBestFitness(self):   
        # la fitness del miglior individuo della popolazione
        return self.individuals[0].getFitness()
    
    def getBestIndividual(self):
        # il miglior individuo della popolazione
        return self.individuals[0].getIndividuals()
    
    def getResults(self):
        # ritorna la miglior fitness e il miglior individuo della popolazione
        return (self.individuals[0].getFitness(),self.individuals[0].getIndividuals())

    def savePopulation(self,file_name):
        # salva su file la popolazione
        import pickle
        with open(file_name, "wb") as fp:
            pickle.dump(self.individuals, fp)
            
    def loadPopulation(self,file_name):
        # carica da file la popolazione
        import pickle
        with open(file_name, "rb") as fp:
            self.individuals = pickle.load(fp)
            
    def printPopulation(self, n=None):
        # stampa dell'intera popolazione di individui o di una sua parte
        print()
        print("\033[2;1H")
        for i,individual in enumerate(self.individuals):
            print('INDIVIDUAL N.%3d '%i,end=" - ")
            individual.printFitness()
            individual.printIndividual()
            if n != None and i >= n:
                break
        print(f"\nPopulation LENGTH: {len(self.individuals)}")
