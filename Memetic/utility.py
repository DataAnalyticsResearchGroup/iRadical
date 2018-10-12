import numpy as np
import collections
import random

def get_degree(v,gmat):
    """ this function return the degree of one node """
    
    return np.count_nonzero(gmat[v][:] != 0)

def get_all_degrees(vertix,gmat):
    """ this function get a list of nodes and return all degres """
    degs= []
    for v in vertix:
        degs.append(get_degree(v,gmat))
        
    return degs    



def cal_2hop(v, gmat) :
    # calcualte 2 hop for one vertix in graph and return result
    # first calcualte one hot and then calculate the second hop
    
    resutl = 0.0 
        ## calculation one hop
  
    adjs = get_neighbors(v, gmat)
    if np.shape(adjs)[0] > 0:
        weights = np.sum(gmat[v][adjs])        
        resutl += np.sum(weights)
        ## calculatoin two hop vertix
        for ad in adjs:
            sec_hop_adjs = get_neighbors(ad, gmat)
            if np.shape(sec_hop_adjs)[0] != 0:
                weights =gmat[v][ad] * np.sum(gmat[ad][sec_hop_adjs])
                resutl += weights
    return resutl    
        #print adjs, weights, resutl
  
    ## calculatoin two hop vertix 
#    for w in range(len(weights)):
#        adj_res, weght_res = find_one_hop_neighbors(adjs[0][w], gmat)
#        
#        if weght_res is not None:             
#            resutl += weights[w] * np.sum(weght_res)
#            
   
    
#def find_one_hop_neighbors(vert_id, gmat):  
#    adjs, weights = [],[]
#    
#    adjs = np.where(gmat[:][vert_id] != 0)
#    #     print "adjs",adjs
#    if adjs is None:
#        return None, None
#    
#    weights = gmat[:][vert_id][adjs]
#    if np.shape(adjs)[0] == 2: 
#        return adjs[1], weights
#    else:
#        return adjs, weights

def get_neighbors(vert_id, gmat):  
    """ return one hip neighbor but without weights
    and return set the neoghbors """
    return np.where(gmat[vert_id] != 0)[0]
    
    
def get_all_neighbors(seed, gmat):
    all_adjs = set()
    
    for vert  in seed:
#        adjs = get_neighbors(vert, gmat)
#        print(adjs)
        all_adjs = all_adjs.union(set(list(get_neighbors(vert, gmat))))
#       
    return list(all_adjs)

#seed= [0,1]
#print (get_all_neighbors(seed, gmat))




def replace_with_correct_item(x, indx, Candidate):
    """ get one index and replace that with new node which is valid node"""
      
    x = list(x)
    left, right = x[:indx], x[indx+1:]
    x_removed_item = left + right        
    length = len(set(x_removed_item)) + 1 # maybe has other repeatation
    new_item = add_valid_random_from_coondidate(x_removed_item,length,Candidate)   
    
    x = left + [new_item] + right  # to put on right position        
    return x

def add_valid_random_from_coondidate(x,length,Candidate):
    """ select 1 node randomly from candidate to add to x and check validity(check to not repeat)"""
    x = set(x)
    Candidate = list(Candidate)
    length = len(x)+1
    while len(x) < length:
        selected = random.sample(Candidate,1)[0]       
        x = x.union(set([selected]))
    return selected


def find_dupplicates(x):
    """ finding dupplicates """
    return [item for item, count in collections.Counter(x).items() if count > 1] 

# def check_Validity(x, length, Candidate, args):
#     """ check is there any repeated value """
#     x = set(x)
#     while len(x) < length:
#         selected = random.sample(Candidate,1)
#         x = x.union(set([selected]))               
#     return x

def sortpopulation(population, fitnesses, args):
    """ sort population based on the fitness minimization or maximation"""
    
    minimization = args['minimization']
    PopulationSize = args['pop_size']
    
    if minimization == False:
        #here we sort the candidates based on fitnesses descending order
        ind = np.argsort([ -x for x in fitnesses])        
    else:
        #here we sort the candidates based on fitnesses ascending order
        ind = np.argsort([ x for x in fitnesses])
        
        
    fitnesses= np.asarray(fitnesses) [ind]
    population= np.asarray(population) [ind]
        
    return population[0:PopulationSize], fitnesses[0:PopulationSize]


def  BestIndividualInitialization(population, fitnesses, args):
    "find the best fitness"
    minimization = args['minimization']
    
    if minimization == True:
        best_ind = np.where(fitnesses == np.min(fitnesses))[0][0]
    else:
        best_ind = np.where(fitnesses == np.max(fitnesses))[0][0]

    return population[best_ind], fitnesses[best_ind]
        

def Similarity(u,v,gmat):
    NBu= set(get_neighbors (u,gmat))
    NBv= set(get_neighbors (v,gmat))
    
    upper = len(NBu.intersection(NBv))
    lower = len(NBu) + len(NBv)
    
    if lower == 0:
        return 0.0
    else:
        return float(upper)/float(lower)
