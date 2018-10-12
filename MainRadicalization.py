import numpy as np
import pickle 

######### read dataset ############## 
import pandas as pd 
data_filename = "tweets.csv"
csv_data = pd.read_csv(data_filename) 
# Preview the first 5 lines of the loaded data 
#csv_data.head(3)
#######################################
	
# merge all tweets
mydf = []
i = 0
counter = 0 
while i < len(csv_data):
    print(counter)
    counter+=1
#    indx =  csv_data['username'][i]
    indx = csv_data.index[csv_data['username'] == csv_data['username'][0]].tolist()
    sumy = "";
    for idx in range(len(indx)):
        j = indx[idx]
        sumy += csv_data['tweets'][j]
     
    A = csv_data['username'][i]
    B = csv_data['location'][i]

    try:
        if np.isnan(B):
            B = "NA"
    except:
        pass
    C = sumy
    mydf.append([A, B, C])  
    
    
    csv_data = csv_data.drop(csv_data.index[indx])
    csv_data = csv_data.reset_index()
    csv_data = csv_data.drop(columns=['index'])
    
    
counter, max_count = 0, 112
i = 0
data,ids,locations = [],[],[]
grph_file = "tweet.gml"

""" reading data from file """
    
full_info= []
for i in range(len(mydf)):  
                
    id_ = mydf[i][0]
    id_full = id_
    country = mydf[i][1]
    locality = country
    summary = mydf[i][2]
    
    ids.append(id_)
    full_info.append([id_, id_full, country, locality, summary])
    counter += 1

   

################### bpso part ###############
gmat = np.zeros((len(ids),len(ids)), dtype = int)
for i in range(len(ids)):
    gmat[0][i] = 1
    for j in range(i+1,len(ids)):
        if full_info[i][3] == full_info[j][3]:
            gmat[i][j], gmat[j][i] = 1, 1

with open(grph_file,'w', encoding='UTF-8') as f:
    pass
    
with open(grph_file,'a+', encoding='UTF-8') as f:
    f.write('Creator "vahid Newman on Wed Jul 26 15:04:20 2006" \n')
    f.write('graph \n')
    f.write('[ \n')
    f.write('directed 0 \n')
    
    for i in range(len(ids)):
        f.write('node \n')
        f.write('[ \n')
        f.write('id '+str(i)+'\n')
        f.write('label "'+ids[i]+'"\n')
        f.write('] \n')
      

    for i in range(len(ids)):
        for j in range(i+1,len(ids)):
            if gmat[i][j] == 1:
                f.write('edge \n')
                f.write('[ \n')
                f.write('source '+str(i)+'\n')
                f.write('target '+str(j)+'\n')
                f.write('] \n')                
                
    f.write('] \n')
            


""" first step include calliung required packages """
import bpso as bp
import numpy as np
from fitness import fitness_bin, fitness_con
from utility import get_all_degrees, decode_input, convert_to_binary
from clusteing import  graph_cluster
import bpso as bp
import pickle
import numpy as np
import math
from fitness import fitness_bin, fitness_con
from utility import get_all_degrees, decode_input, convert_to_binary
from clusteing import  graph_cluster

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
    selected = items[np.where(degs > 20)]
    Candidate.extend(selected)
    
degs = get_all_degrees(Candidate, gmat)
degs= np.asarray(degs)
ind = np.argsort(-degs)
Candidate = np.asarray(Candidate)
Candidate_main = Candidate[ind]
Candidate = range(len(Candidate_main))



args = {}
args['SeedSize'] = 10
args['gmat'] = gmat 
args['MaxIter'] = 5
args['PopSize'] = 30
args['c1'] =  1.5
args['c2'] =  1
args['w'] =  1
args['wdamp'] = 0.995
args['Candidate'] = Candidate 
args['Candidate_size'] =  len(Candidate)

args['SeedSize'] += 1
nVar = math.floor(math.log2(args['Candidate_size']))
if nVar < math.log2(args['Candidate_size']):
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
print(Candidate_main[decode_input(gbest['position'], args)][1:], ' and best cost=', -gbest['cost'])
print()



###################### Read all data from KB #################
#import glob, os
#filepath = "../KnowledgeBases"
#os.chdir(filepath)
#for file in glob.glob("*.txt"):
#    print(filepath+"/"+file)
final_candidate  = Candidate_main[decode_input(gbest['position'], args)][1:]

def get_words(filepath):
    words = []
    with open(filepath) as fp:  
       line = fp.readline()   
       while line:
           words.append(line.strip())
           line = fp.readline()
    return words


filepatheducational = "../KnowledgeBases/KB for educational level.txt"
filepathNeg = "../KnowledgeBases/KB for neg ideas about Western.txt"
filepathorigin = "../KnowledgeBases/KB for origin.txt"
filepathideology = "../KnowledgeBases/KB for political ideology.txt"
filepathracism = "../KnowledgeBases/KB for racism.txt"
filepathterrorismattitude = "../KnowledgeBases/KB for terrorism attitude.txt"
filepathmental = "../KnowledgeBases/KB for mental health.txt"
filepathfrustration = "../KnowledgeBases/KB for frustration.txt"
filepathdiscrimination = "../KnowledgeBases/KB for discrimination.txt"
filepathintroversion = "../KnowledgeBases/KB for introversion.txt"
filepathreligion = "../KnowledgeBases/KB for pos ideas about religion.txt"
filepathpersonality = "../KnowledgeBases/KB for personality traits.txt"
filepathpsychological = "../KnowledgeBases/KB for psychological factors.txt"
   
########################### 
Educational = get_words(filepatheducational)
Negative = get_words(filepathNeg)
Origin = get_words(filepathorigin)
Political = get_words(filepathideology)
Racism = get_words(filepathracism)
Terrorism = get_words(filepathterrorismattitude)
Mental = get_words(filepathmental)
Frustration = get_words(filepathfrustration)
Discrimination = get_words(filepathdiscrimination)
Introversion = get_words(filepathintroversion)
Positive = get_words(filepathreligion)
Personality = get_words(filepathpersonality)
Pychological = get_words(filepathpsychological)

def getrate(summary, words):
    cont = 0 
    
    for wrd in words:
        if wrd in summary:
            cont += 1
    if len(words) == 0:
        return 0
    return float(cont) / float(len(words))                


####################### Item Added ############################
for item in final_candidate:
    id_full = full_info[item][1]
    summary = full_info[item][4]
    
    print("****************************")
    print("User Id :", id_full) 
    print(summary)
    print("\n")
    
    print("educational:", getrate(summary, Educational))
    print("Negative ideas about Western:", getrate(summary, Negative))
    print("origin:", getrate(summary, Origin))
    print("ideology:", getrate(summary, Political))
    #print("attitude:", getrate(summary, attitude))
    print("racism:", getrate(summary, Racism))
    print("terrorismattitude:", getrate(summary, Terrorism))
    print("Mental health:", getrate(summary, Mental))
    print("Frustration:", getrate(summary, Frustration))
    print("Discrimination:", getrate(summary, Discrimination))
    print("Introversion:", getrate(summary, Introversion))
    print("Positive ideas about religion:", getrate(summary, Positive))
    print("Personality traits:", getrate(summary, Personality))
    print("Psychological factors:", getrate(summary, Pychological))
     
    
  
        
    
    
    
    
    
    
    
    
    

