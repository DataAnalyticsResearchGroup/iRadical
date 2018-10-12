from utility import get_neighbors
from fitness import fitness
import collections

def LocalSearch(x, candidate, args):
    x = list(x)
    lenx= len(x)
    gmat = args['gmat']    
    best_fit_local = fitness(x, gmat)
    
    #print ("np.shape(x)",np.shape(x), "x[0]", x[0],"x[1]",x[1], "x[2]",x[2])
    
    for i in range(lenx):        
        local_neighbors = get_neighbors(x[i], gmat)
        for itm in local_neighbors:
            xx =  x[:i]+ [itm] + x[i+1:]
            if len(set(xx)) < lenx:
                continue
            
            new_fit = fitness(xx, gmat)
            if new_fit > best_fit_local:
                best_fit_local = new_fit
                x = xx
                
    return x, best_fit_local    