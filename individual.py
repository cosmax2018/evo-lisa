
# individual.py : simple GA v.2 written in Python (slow version)
#
#    (c) Copyright 2020-25 by ....@_°° Lumachina SW
#    Massimiliano Cosmelli (massimiliano.cosmelli@gmail.com)

from random import choice, randint

class Individual():
    # classe di inizializzazione o costruttore
    def __init__(self,alphabet,individualLength,objectiveFunction):
        self.alphabet           = alphabet          # alfabeto
        self.individualLength   = individualLength  # length of the individual
        self.objectiveFunction  = objectiveFunction # funzione obiettivo utilizzata per il calcolo della fitness

        self.fitness            = 0                 # la fitness
        self.individual         = []                # il cromosoma dell'individuo
        
    def get(self):              return self.individual
    
    def getIndividual(self,i):  return self.individual[i]                                # restituisce il gene i-esimo

    def setIndividual(self,i,v):self.individual[i] = v                                   # setta il gene i-esimo
    
    def getIndividuals(self):   return self.individual                                  # restituisce tutti i geni
    
    def setIndividuals(self,v): self.individual = v                                     # setta tutti i geni
    
    def getFitness(self):       return self.fitness                                     # restituisce la fitness
    
    def setFitness(self):       self.fitness = self.objectiveFunction(self.individual)  # calcola la fitness

    def rnd_value(self):        return choice(self.alphabet)
    
    def rndIndividual(self):
        # genera un individuo a caso
        self.individual = []
        r,g,b = self.rnd_value(),self.rnd_value(),self.rnd_value()
        x1,y1 = self.rnd_value(),self.rnd_value()
        x2,y2 = randint(x1,randint(x1,self.alphabet[-1])), randint(y1,randint(y1,self.alphabet[-1]))
        for i in range(self.individualLength):
            individual = (
                          (r,g,b),
                          (x1,y1),
                          (x2,y2)
                         )
            self.individual.append(individual)
    
    def mutateIndividual(self):
        # genera una mutazione casuale
        r,g,b = self.rnd_value(),self.rnd_value(),self.rnd_value()
        x1,y1 = self.rnd_value(),self.rnd_value()
        x2,y2 = randint(x1,randint(x1,self.alphabet[-1])), randint(y1,randint(y1,self.alphabet[-1]))        
        # print(self.individual[randint(0,self.individualLength-1)])
        self.individual[randint(0,self.individualLength-1)] = (
                                                                (r,g,b),
                                                                (x1,y1),
                                                                (x2,y2)
                                                               )
    
    def crossoverIndividuals(self,parent):
        # incrocia i cromosomi di due individui ottenendo altri due cromosomi figli
        child1,child2 = [],[]
        crossOverPoint = randint(1,self.individualLength-1)
        for i in range(self.individualLength):
            if i < crossOverPoint:
                child1.append(self.individual[i])
                child2.append(parent.individual[i])
            else:
                child1.append(parent.individual[i])
                child2.append(self.individual[i])
        return (child1,child2)
    
    def printFitness(self):
        # stampa la fitness
        print('FITNESS: %5f '%self.fitness,end=' - ')
        
    def printIndividual(self):
        # stampa il cromosoma
        print('INDIVIDUAL: ',end='')
        for i in range(self.individualLength):
            print(self.individual[i],end=',')
        print(f"Individual LENGTH: {len(self.individual)}")
        
        