from fitness import fitness_con
from utility import get_all_degrees, get_neighbors, decode_input, convert_to_binary

def LocalSearch(x, candidate, args):
    x = decode_input(x, args)
        
    
    x = list(x)
    lenx= len(x)
    gmat = args['gmat']  
    
    best_fit_local = fitness_con(x, args)
    
     
    for i in range(lenx):        
        local_neighbors = get_neighbors(x[i], gmat)
        for itm in local_neighbors:
            xx =  x[:i]+ [itm] + x[i+1:]
            if len(set(xx)) < lenx:
                continue
            
            new_fit = fitness_con(xx, args)
            
            if new_fit < best_fit_local:
                best_fit_local = new_fit
                x = xx
                
    return x, best_fit_local    