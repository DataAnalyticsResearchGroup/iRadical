import numpy as np
from utility import get_neighbors, get_all_degrees, Similarity
        



#Algorithm 3 SHD algorithm.
def SHD(Candidate,k,gmat,sim=0.9):
    #1: Start with xa = None;
    #2: TempCandidate = Candidate;    
    if len(Candidate) < k:
        print("error in SHD : len(Candidate) < k " )
        return
        
    xa = set()
    
    degrees = get_all_degrees(Candidate,gmat)    
    TempCandidate = Candidate
    #print(degrees, TempCandidate) 
    
    #here we sort the candidates based on degrees descending order
    ind = np.argsort([ -x for x in degrees])
    #degrees= np.asarray(degrees)[ind]
    TempCandidate= np.asarray(TempCandidate) [ind]
    #print(degrees, TempCandidate) 
         
    #3: for i from 1 to k do
    #4: choose a node vi ! TempCandidate with the highest
    #degree;
    #5: xa ! xa , "vi,;
    for i in range(k):
        v = TempCandidate[0]        
        xa = xa.union(set([v]))        
        TempCandidate = np.delete(TempCandidate,0)        
        #6: SimNeighbor ! "u ! N^vh | Similarity^u,vh $ sim,;
        SimNeighbor = set()
        for u in get_neighbors(v,gmat):            
            if Similarity(u,v,gmat) >= sim :
                SimNeighbor = SimNeighbor.union(set([u]))
                #print("SimNeighbor",SimNeighbor)
        
        #7: TempCandidate !
        #"v | v ! TempCandidate,v " SimNeighbor,v ! vi,;        
        for s in SimNeighbor:
            for r in range(len(TempCandidate)):
                if s ==  TempCandidate[r]:
                    TempCandidate = np.delete(TempCandidate,r)
                    break
        
        if len(TempCandidate) == 0:
            break
            
        #8: if TempCandidate = Q do
        #9: xa ! xa , "vi+ 1,vi+ 2,g,vk,,vi+ 1,vi+ 2,g,vk are selected
        #from Candidate randomly; 
         #10: break;
        #11: end if
        #12: end for
    while len(xa) < k:
          xa = xa.union(set([Candidate[np.random.randint(0,len(Candidate))]]))
               
    return list(xa)

#k = 5
#Candidate = list(range(0,20))
#print(SHD(Candidate,k,gmat,sim=0.3))

# # myset = set([4, 5, 3, 0, 0, 4])
#a,b =  find_one_hop_neighbors([6], gmat)
#print a
#print b