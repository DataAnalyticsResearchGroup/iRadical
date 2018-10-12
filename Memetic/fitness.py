import numpy as np
from utility import cal_2hop, get_all_neighbors

def fitness(seed, gmat):
    seed = list(seed)
    #print ("seed",type(seed), np.shape(seed))
    # this function calculate the fitness of a seed
    # the equation and formula is in p1 to p4 !!!
    # the main equation is breakdown to some equation and finally they are 
    # calculated one by one
    
    # input sees is a list of vertex
    
    p = gmat # weight or probablity of graph
    ##### term1 calculation
    term1 = 0.0 
    for vert in seed: # equal to for s in S (sigma s member of S)
        term1 += cal_2hop(vert, gmat)   
    
       
    
    ##### term2 calculation
    term2 = 0.0
    cs = get_all_neighbors(seed, gmat)
    S = set(seed)
    CS = set(cs)
    S_intersect_Cs = S.intersection(CS)
    #print "S_intersect_Cs",S_intersect_Cs
    
    for s in S:
        for c in S_intersect_Cs:
            if p[s][c] == -1:
                continue
            else:
                p_s_c = p[s][c]
                
            if p[c][s] == -1:
                p_c_s = 0
            else:
                p_c_s = p[c][s]                
            sigma_1_val = sigma_hat(c, gmat)  
            term2 += p_s_c * (sigma_1_val - p_c_s)
           
        
      
    
    ##### term3 calculation
    term3 = 0.0
    S = set(seed)   
    for x in S:        
        cx = get_all_neighbors([x], gmat)        
        for y in S.intersection(set(cx)):
            cy = get_all_neighbors([y], gmat)            
            D = S.intersection(set(cy)).difference(set([x])) 
            
            for d in D :
                
                
                if p[x][y] == -1:
                    p_x_y = 0
                else:
                    p_x_y = p[x][y]
                
                if p[y][d] == -1:
                    p_y_d = 0
                else:
                    p_y_d = p[y][d]
                    
                term3 += p_x_y  * p_y_d
        
            
    #print (term1,term2,term3)
    #print("term1 - term2 - term3",term1 - term2 - term3)
    return term1 - term2 - term3
    
def sigma_hat(vertu, gmat):
    result = 1.0
    xk = get_all_neighbors([vertu], gmat)      
    for x in xk:        
        result += gmat[vertu][x]          
    
    return result


def cal_fitnesses(population, args):
    """ get a set of population and calculate all fitneeses and return the fitness values"""
    
    gmat = args['gmat']
    fitnesses = np.zeros((len(population),1))
    
    
    for i in range(len(population)):
        fitnesses[i] = fitness(population[i][:], gmat)
    
    return fitnesses
    

#print (fitness([0,2,3], gmat))

