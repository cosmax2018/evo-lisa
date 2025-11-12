
# ga.py : simple GA v.2 written in Python (slow version)
#
#    (c) Copyright 2020-25 by ....@_°° Lumachina SW
#    Massimiliano Cosmelli (massimiliano.cosmelli@gmail.com)

from population import Population
# from population_multiprocessing import Population    # multi-processes version. (anche se riesce a saturare tutti i cores della cpu sembra molto più lenta della versione non multiprocessing)
import time

def timer(function):                        # prende come parametro la funzione di cui misurare il tempo di esecuzione
    def timed(*args):                        # args sono i parametri passati alla funzione da misurare
        start_time = time.time()            # Ti
        result = function(*args)            # esegue la funzione
        elapsed = time.time() - start_time    # Tf
        print('Function "{name}" took {time} seconds to complete.'.format(name=function.__name__, time=elapsed))
        return result                        # restituisce il risultato dell'esecuzione della funzione
    return timed
    
class Simple_GA:
    # classe di inizializzazione o costruttore
    def __init__(self,populationSize, tournamentSize, mutationRate, alphabet, chromosomeLength, objectiveFunction):
        self.REPLACE_EVERY      = 100
        self.populationSize     = populationSize
        self.tournamentSize     = tournamentSize
        self.mutationRate       = mutationRate
        self.alphabet           = alphabet
        self.chromosomeLength   = chromosomeLength
        self.objectiveFunction  = objectiveFunction
        
        self.population         = Population(populationSize,tournamentSize,mutationRate,alphabet,chromosomeLength,objectiveFunction)    # una popolazione di individui
        
    def getWorstFitness(self):          return self.population.getWorstFitness()
    
    def getBestFitness(self):           return self.population.getBestFitness()
    
    def getBestIndividual(self):        return self.population.getBestIndividual()
    
    def getResults(self):               return self.population.getResults()
    
    def getIndividuals(self):           return self.population.getIndividuals()
    
    def savePopulation(self,file_name): return self.population.savePopulation(file_name)    
    
    def loadPopulation(self,file_name): return self.population.loadPopulation(file_name)
    
    def replaceWhorst(self,threshold):  return self.population.replaceWhorst(threshold)
    
    def newRndPopulation(self):         return self.population.rndPopulation()
    
    def sortPopulation(self):           return self.population.sortPopulation()
    
    def evaluatePopulation(self):       return self.population.evaluatePopulation()
    
    def mutatePopulation(self):         return self.population.mutatePopulation()
    
    def evolvePopulation(self):         return self.population.evolvePopulation()
    
    def printPopulation(self,n=None):   return self.population.printPopulation(n)
    
    def evaluate_thread(self):          self.population.evaluatePopulation()        # evaluating population fitness
    
    def sort_thread(self):              self.population.sortPopulation()            # sorting population by fitness
    
    def evolve_thread(self):            self.population.evolvePopulation()          # evolving population
    
    def mutate_thread(self):            self.population.mutatePopulation()          # mutating population        

    def stepGa(self):                                                               # execute one single step
        
        self.population.evaluatePopulation()

        self.population.sortPopulation()

        self.population.evolvePopulation()

        self.population.mutatePopulation()
        
    @timer
    def runGa(self, maxIterations, threshold=0, m=20):                              # esegue l'algoritmo genetico
                
        print("\033[1;1HITERATION: ")
        
        for iterations in range(maxIterations):
            
            print("\033[1;12H" + str(iterations))
            
            self.stepGa()
            
            self.population.printPopulation(m)          # stampa i primi m individui della popolazione
            
            if iterations % self.REPLACE_EVERY == 0:    # ogni tot. iterazioni rimpiazza gli individui con fitness < fitness minima (Es threshold = 30) con nuovi individui creati a caso
                if threshold != 0:
                    self.population.replaceWhorst(threshold)
                    