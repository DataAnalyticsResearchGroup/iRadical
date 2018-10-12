
""" first step include calliung required packages """
import pickle
import numpy as np
#import networkx as nx

from fitness import cal_fitnesses
from fitness import fitness
from utility import get_all_degrees, BestIndividualInitialization, sortpopulation
from local_search import LocalSearch
from pop_initial import PopulationInitialization
from genetic_fun import GeneticOperation, Selection
from clusteing import  graph_cluster
 
''' also we key in the constant values include graph address '''
grph_file = "dolphins/dolphins.gml"

""" second step is loading the graph, can be from any kind of files or can be as the cached pickle file"""
#import igraph
#grph = igraph.Graph.Read_GML(grph_file)
#ugraph = grph.as_undirected()
#fgmat = ugraph.get_adjacency()
#gmat = np.asarray(fgmat.data)

 
#with open('gmat_dolphn.pck', 'wb') as f:
#    pickle.dump(gmat,)
with open('gmat_dolphn.pck', 'rb') as f:
    gmat = pickle.load(f)


""" choosing the candidates, this part is done by using the clustring techniques"""

pyl = graph_cluster.from_gml_file(grph_file)
partition, q = pyl.apply_method()
        
 

""" calculatin degree and selecting based on the best degrees in each group"""
""" ******  modification in this part can affect the result ****** """
Candidate = []
for items in partition:
    items = np.asarray(items)
    degs = get_all_degrees(items, gmat)      
    degs= np.asarray(degs)
    #ind = np.argsort(-degs)
    #sorted_items = np.asarray(items)[ind]
    selected = items[np.where(degs > 2)]
    Candidate.extend(selected)
    
degs = get_all_degrees(Candidate, gmat)
degs= np.asarray(degs)
ind = np.argsort(-degs)
Candidate = np.asarray(Candidate)
Candidate = Candidate[ind]


#Table 1 The variables used in this paper.
#Variables Descriptions
#G(V, E) An undirected network with node set V and edge set E
#N The number of nodes in G
#M The number of edges in G
#k The number of seeds ^1 # k # Nh
#S The seed set with k-node
#p Propagation probability


"""  here is the body of memetic algorithm , using genetic functinality """
#Framework of Meme-IM.
def Meme_IM(args):
     
    Candidate = args['Candidate']    
    MaximumGeneration = args['maxgen']
    PopulationSize = args['pop_size']
    MatingPoolSize = args['pool']
    TournamentSize = args['tour']
    CrossoverProbability = args['pc']
    MutationProbability = args['pm']
    SpreadProbability = args['p']
    SeedSize = args['k']
    TheCandidateNodesPool = args['Candidate']
    TheConnectionMatrix = args['A']
    NumberOfGenerations = args['NumberOfGenerations']
    gmat = args['gmat']
    
    pop_x = args['pop_size']
    pop_y = SeedSize
    ### should be removed only for test
    
    #    1:Step 1) Initialization
    #    3: Step 1.2) Best individual initialization: Pbest = xi ;
    population = PopulationInitialization(args)
    population = np.reshape(population, (pop_x,pop_y))
    
    fitnesses = cal_fitnesses(population, args)
    fitnesses = np.reshape(fitnesses, (pop_x))
    
    population, fitnesses = sortpopulation(population, fitnesses, args)
     
    Pbest,_ = BestIndividualInitialization(population, fitnesses, args)
    
      
    #    4: Step 2) Set t = 0; // the number of generations
    #    5: Step 3) Repeat
    #    6: Step 3.1) Select parental chromosomes for mating;
    #    Pparent ! Selection(P, pool, tour);
    #    7: Step 3.2) Perform genetic operators:
    #    Pchild ! GeneticOperation(Pparent , pc, pm);
    #    8: Step 3.3) Perform local search:
    #    Pnew ! LocalSearch(Pchild );
    #    9: Step 3.4) Update population:
    #    P ! UpdatePopulation(P, Pnew );
    #    10: Step 3.5) Update the best individual Pbest ;
    #    11: Step 4) Stopping criterion: If t < maxgen, then
    #    t = t +1 and go to Step 3), otherwise, stop the
    #    algorithm and output.

    for t in range(MaximumGeneration):
        #print("generation = ", t)
                
        Pparent = Selection(population,fitnesses, TournamentSize, args)
        
        Pparent, fit  = LocalSearch(Pparent, Candidate, args)
        cross_child1, cross_child2, mute_child1,mute_child2  = GeneticOperation(Pbest, Pparent, Candidate, args)
#        cross_child1, fitc1 = LocalSearch(cross_child1, Candidate, args)
#        cross_child2, fitc2 = LocalSearch(cross_child2, Candidate, args)
#        mute_child1,  fitm1 = LocalSearch(mute_child1, Candidate, args)
#        mute_child2,  fitm2 = LocalSearch(mute_child2, Candidate, args)
#        
        
        fitc1 = fitness(cross_child1, gmat)
        fitc2 = fitness(cross_child2, gmat)
        fitm1 = fitness(mute_child1, gmat)
        #fitm2 = fitness(mute_child2, gmat)
        
        #print(cross_child1, cross_child2,mute_child1,mute_child2)
       
        population,fitnesses = list(population), list(fitnesses)
        population.append(cross_child1)
        fitnesses.append(fitc1)
        population.append(cross_child2)
        fitnesses.append(fitc2)
        population.append(mute_child1)
        fitnesses.append(fitm1)
        #population.append(mute_child2)
        #fitnesses.append(fitm2)
        
        
        population, fitnesses = np.asarray(population), np.asarray(fitnesses)
        population, fitnesses = sortpopulation(population, fitnesses, args)
        Pbest,_ = BestIndividualInitialization(population, fitnesses, args)
        
        #print("fitnesses",fitnesses)
        print("Generation:",t," best fitnesses", fitnesses[0])
        
    return population[0], fitnesses[0]
#best_candidate, best_fitness = Meme_IM(args)
################################### Main Part #################################
""" program is started from this point, so we set all the required argument in this part"""    

args = {}
args['gmat'] = gmat 
args['maxgen'] = 50 #50
args['pop_size'] = 20 #200
args['k'] = 10

args['pool'] = 10 # 100
args['tour'] = 4 
args['pc'] = 0.8
args['pm'] = 0.1
args['p'] = 0.2
args['Candidate'] = Candidate
args['A'] =  []
args['NumberOfGenerations'] = args['maxgen']
args['sim_rate'] = 0.6    
args['cadidate_size'] =  47
args['minimization'] = False


"""  after setting the arguments and parameters, the main part is run using bellow command"""
best_candidate, best_fitness = Meme_IM(args)


""" just printing final result """
print("best fitness = ",best_fitness)
print("best candidate = ",best_candidate)







