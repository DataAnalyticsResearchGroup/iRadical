import numpy as np
import collections
from utility import find_dupplicates, replace_with_correct_item, BestIndividualInitialization

def crossover_one_point(ind1, ind2, Candidate):
    ind1,ind2 = list(ind1),list(ind2) 
    
    #print("ind1,ind2",ind1,ind2,len(ind1))
    
    cross_point = np.random.randint(1, len(ind1)) 
    
    ind1[cross_point:], ind2[cross_point:] = ind2[cross_point:], ind1[cross_point:]
    
    ### check validity of the members to add ###
       
    x = ind1
    itms = find_dupplicates(x)    
    for itm in itms:
        indx = np.where( np.asarray(x) == itm)[0][-1]
        x = replace_with_correct_item(x, indx, Candidate)
    ind1 = x
    
    x = ind2
    itms = find_dupplicates(x)    
    for itm in itms:
        indx = np.where( np.asarray(x) == itm)[0][-1]
        x = replace_with_correct_item(x, indx, Candidate)
    ind2 = x    
    return ind1,ind2


def muttate (x, Candidate, args):
    """ need to be complited """
    pm = args['pm']
    for indx in range(np.shape(x)[0]):
        r = np.random.random()
        if r < pm:
            x = replace_with_correct_item(x, indx, Candidate)
    return x               
                   

def GeneticOperation(Pbest, Pparent , candidate, args):
    
    pc = args ['pc']   
    
    if np.random.random() < pc :       
        cross_child1, cross_child2 = crossover_one_point(Pbest, Pparent, candidate)
    else:
        cross_child1, cross_child2 = Pbest, Pbest
        
    mute_child1 = muttate (cross_child1, candidate, args )
    mute_child2 = muttate (cross_child2, candidate, args )
        
    return cross_child1, cross_child2, mute_child1, mute_child2  

def Selection(population, fitnesses, tour, args):    
    ind = np.random.randint(1,len(fitnesses),tour)   
    bestpop, _ = BestIndividualInitialization(population[ind], fitnesses[ind], args)   
    return bestpop 




