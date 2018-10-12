""" first step include calliung required packages """
import bpso as bp
import pickle
import numpy as np
import math

from fitness import fitness_bin, fitness_con
from utility import get_all_degrees, decode_input, convert_to_binary
from clusteing import  graph_cluster



''' also we key in the constant values include graph address '''
grph_file = "dolphins/dolphins.gml"

""" second step is loading the graph, can be from any kind of files or can be as the cached pickle file"""
#import igraph
#grph = igraph.Graph.Read_GML(grph_file)
#ugraph = grph.as_undirected()
#fgmat = ugraph.get_adjacency()
#gmat = np.asarray(fgmat.data)


global gmat 
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




args = {}
args['SeedSize'] = 10
args['gmat'] = gmat 
args['MaxIter'] = 1000
args['PopSize'] = 20 
args['c1'] =  1.5
args['c2'] =  1
args['w'] =  1
args['wdamp'] = 0.995
args['Candidate'] = Candidate 
args['Candidate_size'] =  len(Candidate)

nVar = math.floor(math.log2(args['Candidate_size']))
if nVar < math.sqrt(args['Candidate_size']):
    nVar += 1

args['len_var'] = nVar
args['nVar'] = nVar * args['SeedSize'] 

    
problem = {
        'CostFunction': fitness_bin,
        'nVar': args['nVar']  ,
        'VarMin': 0,   
        'VarMax': 1,   
    }
        
args['problem'] = problem         
        
# Running bPSO
gbest, pop = bp.bPSO(args)

# Final Result
print('Global Best:')
print(decode_input(gbest['position'], args), ' and best cost=', -gbest['cost'])
print()






