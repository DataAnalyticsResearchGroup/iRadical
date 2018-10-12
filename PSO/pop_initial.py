import numpy as np
import random
from shd import SHD
#Algorithm 2 Population initialization.
#Input: Population size: pop
#Output: Population P
def PopulationInitialization(args):    
     
    PopulationSize = args['pop_size']
    SeedSize = args['k']
    gmat = args['gmat']
    sim_rate = args['sim_rate']
    cadidate_size = args['cadidate_size']
    
    #1: Generate a half of population based on SHD, see
    #Algorithm 3 for more information;  
    population = np.ones((PopulationSize,SeedSize), dtype= np.uint32) * -1 
    all_candidate = range(0,cadidate_size)
    for i in range(PopulationSize):
        Candidate = random.sample(all_candidate, cadidate_size)
        population[i] = SHD(Candidate, SeedSize, gmat, sim= sim_rate)
        
            
         
    #2: for i from 1 to ^pop/2h do
    #3: for j from 1 to k do
    #4: if rand^1h2 0.5 then
     #5: select a random node different from each node in xi
    #from the Candidate to replace xi
    #j ;
    #6: end if
    #7: end for
    #8: end for
    for i in range(int(PopulationSize/2)):   
        one_sampel = set(population[i])
        for j in range(SeedSize):
            if np.random.random() > 0.5 :
                #                 print "population",population
                #                 print "range(SeedSize)",range(SeedSize)
                #                 print "one_sampel", one_sampel
                #                 print i,j, population[i][j]
                #print "set(population[i][j])",set([population[i][j]])
                
                
                one_sampel = one_sampel.difference(set([population[i][j]])) 
                
                while len(one_sampel) < SeedSize:
                    selected_itm = random.sample(all_candidate, 1)
                    one_sampel = one_sampel.union(selected_itm)
                
                #print "selected_itm",selected_itm[0]
                population[i][j] = selected_itm[0]
                #5: select a random node different from each node in xi from the Candidate to replace xi
                 
     
    #9: for i from ^pop/2 + 1h to pop do
    #10: select k different nodes from the Candidate to
    #initialize xi based on SHD;
    #11: end for
    #for i in range(int(PopulationSize/2),PopulationSize):
        #SelectKdifferentNodesFromCandidateToInitializeSHD()
    ## this section is done in first part, we initial all population using SHD then change the hal of the initial population     
         
    return population
