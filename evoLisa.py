
#####################################################################
#                                                                   #
# evoLisa.py : Painting Monnalisa ..and other characters, with a GA #
#                                                                   #
#####################################################################
#	 (c) Mit license 2020-25 by ....@_°° Lumachina Software         #
#    Massimiliano Cosmelli (massimiliano.cosmelli@gmail.com)        #
#####################################################################

import time,os,argparse,itertools
from PIL import Image                                                       # the graphic library
from images import SuperImposeNewRectangleRGBA,ColourDistanceSquaredRGBA    # manipulate graphic primitives and measures the color distance
from ga import Simple_GA                                                    # the Genetic Algorithm !

XRES,YRES = 160,200
COLOR,POINT1,POINT2 = 0,1,2
R,G,B,A = 0,1,2,3
X,Y = 0,1

ALPHABET            = tuple([i for i in range(255)])
NUM_OF_RECTANGLES   = 50
MAX_ITERATIONS      = 10_000
POPULATION_SIZE     = 100
TOURNAMENT_SIZE     = 6
MUTATION_RATE       = 0.25
SAVE_EVERY          = 100               # save results every tot iterations
REPLACE_EVERY       = 100               # replace worst individuals every tot iterations
FITNESS_THRESHOLD   = 0.50              # individuals under this fitness percentage value (between max fitness and min fitness) are replaced with random-created ones

MAX_DISTANCE = 40704.5 #65025               # max color distance
MIN_DISTANCE = 8064.5                       # min color distance
DISTANCE_RANGE = MAX_DISTANCE-MIN_DISTANCE  # difference between max & min color distances

def randomize(): random.seed(time.time())

def timer(function):                            
    # prende come parametro la funzione di cui misurare il tempo di esecuzione
    def timed(*args):
        # args sono i parametri passati alla funzione da misurare
        start_time = time.time()
        result = function(*args)
        elapsed = time.time() - start_time
        print('Function "{name}" took {time} seconds to complete.'.format(name=function.__name__, time=elapsed))
        return result
    return timed
    
def command_line_parser():
    parser = argparse.ArgumentParser(description='Approssima una immagine utilizzando gli algoritmi genetici')
    parser.add_argument("-fname" , help="nome del file dell'immagine target da approssimare")
    args = parser.parse_args()
    if args.fname:
        fileNameAndPath = args.fname
    else:
        fileNameAndPath = 'D:/images/Monnalisa/Monnalisa_160x200.png'
    return fileNameAndPath
    
def decodeImage_test(individuals,canvas_dim):
    # decodifica l'immagine originariamente presente in individual ora trasformato in un vettore di numeri x
    prev_image = Image.new('RGBA',canvas_dim)
    for individual in individuals:                   # ciclo sui numeri che servono per definire tutti i rettangoli
        
        # print(individual)
        
        chromosome = individual #.get()[0]
        
        colors,P1,P2 = chromosome[COLOR],chromosome[POINT1],chromosome[POINT2]
        
        # color = (colors[R]%256,colors[G]%256,colors[B]%256,colors[A]%256) # colore R,G,B,A
        # rect = ((P1[X],P1[Y]),(P2[X],P2[Y]))              # ((x1,y1),(x2,y2))
        
        color = (colors[R]%256,colors[G]%256,colors[B]%256,128)     # colore R,G,B,A e canale alfa fissato ad A = 128 (trasparenza 50%)
        x1,y1,x2,y2 = P1[X],P1[Y],P2[X],P2[Y]
        rect = ((x1,y1),(x2,y2))
        
        # print(f"(R,G,B):{colors}\t(P1,P2):{P1,P2}\tCOLOR: {color}\tRECT:({x1,y1})-({x2,y2})")
        
        image,rect = SuperImposeNewRectangleRGBA(prev_image,rect,color,canvas_dim)
        prev_image = image
    return prev_image

def fitness_test(individual):
    # utilizzando il metodo ColourDistanceSquared della libreria images.py
    # calcola quanto 'fitta' un immagine rispetto a un altra
    # la distanza di colore al quadrato varia fra i valori 8064.6 (=MIN_DISTANCE) e 40704.5 (=MAX_DISTANCE)
    # se l'immagine di riferimento (target) ha una trasparenza nulla 0% (A = 255)
    # e se l'immagine che approssima il target ha una trasparenza del 50% (A = 128)
    
    # print(XRES,YRES)
    # quit()
    
    test_image = decodeImage_test(individual,(XRES,YRES))
    pixels = test_image.load()    # le due immagini devono avere la stessa dimensione!
    
    F = 0.0    # somma delle distanze
    
    for x,y in itertools.product(range(XRES),range(YRES)):
        F += (MAX_DISTANCE - ColourDistanceSquaredRGBA(pixels[x,y],pixels_target[x,y]))/DISTANCE_RANGE
                
    return F/(XRES*YRES)    # divido per il numero di punti contenuti nell'area dell'immagine per fare una media delle fitness
    
def objective_test(individual):
    # calcola la fitness rispetto all'obiettivo
    return fitness_test(individual)
    
#################################################################################################
#                                                                                               #
# usage :   py evoLisa.py -fname d:/images/Monnalisa/Monnalisa_160x200.png                      #
#                                                                                               #
#################################################################################################

fileNameAndPath = command_line_parser()

workDir = os.path.dirname(fileNameAndPath)         # extract the  dir name  (e.g.:'d:/images/Monnalisa/')
fileName = os.path.basename(fileNameAndPath)       # extract the name (e.g.:'Monnalisa_160x200.png')

fileGAGenerated_NameAndPath         = os.getcwd()+'/GA_generated/'+fileName
populationGAGenerated_NameAndPath   = f"{workDir}/GA_population__ITER_{str(MAX_ITERATIONS)}.txt"

if os.path.exists(fileNameAndPath):
    
    print(f"\n\nPainting with a GA {fileNameAndPath}")
    
    image_target = Image.open(fileNameAndPath)     # carica l'immagine target
    image_target.putalpha(255)                     # aggiunge/sovrascrive il canale alfa della trasparenza con valore 255 (opaco al 100%)
    pixels_target = image_target.load()            # carica i pixels dell'immagine target    
    XRES,YRES = image_target.size                  # the image dimensions
    print(XRES,YRES)
    
    #
    #        come vengono codificati TRE rettangoli.
    #                         (R,G,B)   (x1,y1)  (x2,y2)
    #        individuals = (
    #                       ((50,150,30),(50,50),(120,150)),
    #                       ((100,250,130),(10,20),(80,50)),
    #                       ((200,0,0),(80,20),(150,180))
    #                      )
    #
    
    # initialize GA:
    ga = Simple_GA( POPULATION_SIZE,
                    TOURNAMENT_SIZE,
                    MUTATION_RATE,
                    ALPHABET,
                    NUM_OF_RECTANGLES,
                    objective_test
                  )
                  
    # genera gli individui casualmente
    ga.newRndPopulation()
    
    bestFitness    = []
    iteration = 0
    
    while True:
        
        t = time.time()

        ga.stepGa()    # fai una iterazione
        
        bestFitness.append(ga.getBestFitness())
        bestIndividual = ga.getBestIndividual()
            
        if iteration % SAVE_EVERY == 0:
            image = decodeImage_test(bestIndividual,(XRES,YRES))
            image.save(f"{workDir}/{fileName}__ITER{str(iteration)}__POP{str(POPULATION_SIZE)}__RECT{str(NUM_OF_RECTANGLES)}__FIT{str(int(10000*bestFitness[iteration])/100)}.png")
            
        if iteration % REPLACE_EVERY == 0:
            min_fitness = ga.getWorstFitness()
            max_fitness = ga.getBestFitness()
            replace_under_fitness = min_fitness + FITNESS_THRESHOLD*(max_fitness - min_fitness)
            ga.replaceWhorst(replace_under_fitness)
            print(f"Worst fitness is {min_fitness}")
            print(f"Best fitness is {max_fitness}")
            print(f"Individuals under fitness {replace_under_fitness} are replaced.")
            
        print(f'ITERATION N.{iteration} Best Fitness is {bestFitness[iteration]} Time elapsed : {int(time.time()-t)} sec.')                
        iteration += 1

        if iteration == MAX_ITERATIONS:
            break
            
    ga.savePopulation(populationGAGenerated_NameAndPath)
    print(f"\n\nGA Generated paintings saved in {fileGAGenerated_NameAndPath}")
    print(f"GA Generated Population saved in {populationGAGenerated_NameAndPath}")
    
else:
    print(f"Error: {fileNameAndPath} ...no such file or directory.")
