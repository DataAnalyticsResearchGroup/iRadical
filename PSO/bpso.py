
import numpy as np;
from local_search import LocalSearch
from utility import decode_input, convert_to_binary, decimal_to_binary

       

# Particle Swarm Optimization
def bPSO(args):   
    
    MaxIter = args['MaxIter']
    PopSize = args['PopSize'] 
    c1 = args['c1'] 
    c2 = args['c2']
    w = args['w'] 
    wdamp = args['wdamp']  
    problem = args['problem']
    Candidate = args['Candidate']

    # Empty Particle Template
    empty_particle = {
        'position': None,
        'velocity': None,
        'cost': None,
        'best_position': None,
        'best_cost': None,
    };

    # Extract Problem Info
    CostFunction = problem['CostFunction'];
    VarMin = problem['VarMin'];
    VarMax = problem['VarMax'];
    nVar = problem['nVar'];

    # Initialize Global Best
    gbest = {'position': None, 'cost': np.inf}

    # Create Initial Population
    pop = [];
    for i in range(0, PopSize):
        pop.append(empty_particle.copy());
        pop[i]['position'] = np.random.uniform(VarMin, VarMax, nVar)
        # convert to binary
        pop[i]['position'] = convert_to_binary(pop[i]['position'])    
        
        pop[i]['velocity'] = np.zeros(nVar)
        pop[i]['cost'] = CostFunction(pop[i]['position'], args );
        pop[i]['best_position'] = pop[i]['position'].copy()
        pop[i]['best_cost'] = pop[i]['cost'];
        
        if pop[i]['best_cost'] < gbest['cost']:
            gbest['position'] = pop[i]['best_position'].copy()
            gbest['cost'] = pop[i]['best_cost'];
    
    # PSO Loop
    for it in range(0, MaxIter):
        for i in range(0, PopSize):
            
            pop[i]['velocity'] = w*pop[i]['velocity'] \
                + c1*np.random.rand(nVar)*(pop[i]['best_position'] - pop[i]['position']) \
                + c2*np.random.rand(nVar)*(gbest['position'] - pop[i]['position'])

            pop[i]['position'] += pop[i]['velocity']
            
            # convert to binary
            #pop[i]['position'] = convert_to_binary(pop[i]['position']) 
            
            pop[i]['position'] = np.maximum(pop[i]['position'], VarMin)
            pop[i]['position'] = np.minimum(pop[i]['position'], VarMax)
            

            pop[i]['cost'] = CostFunction(convert_to_binary(pop[i]['position']), args)
           
            
            local_n, fit_local = LocalSearch(pop[i]['position'], Candidate, args)
            
            if  fit_local < pop[i]['cost']:
                count = 0
                for itm in local_n:
                    bin_item = decimal_to_binary(itm, args['len_var'])
                    pop[i]['position'][count:count+args['len_var']] = [int(x) for x in bin_item]
                    #print("L", pop[i]['position'][count:count+args['len_var']])
                    count += args['len_var']
                pop[i]['cost'] = fit_local
            
            if pop[i]['cost'] < pop[i]['best_cost']:
                pop[i]['best_position'] = pop[i]['position'].copy()
                pop[i]['best_cost'] = pop[i]['cost']

                if pop[i]['best_cost'] < gbest['cost']:
                    gbest['position'] = pop[i]['best_position'].copy()
                    gbest['cost'] = pop[i]['best_cost']

        w *= wdamp;
        print('Iteration {}: Best Cost = {}'.format(it, -gbest['cost']))

    return gbest, pop
