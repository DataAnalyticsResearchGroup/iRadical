import random 

#we want to creare 2000 randome edge among the accounts
NUM_EDG = 250

def gen_rand():

    data = []
    grph_file = "tweet.json"
    sample_num = 0
    line_num = 0
    with open(grph_file, encoding="utf8") as f:
        lines = f.readlines()
        for line in lines:
            if '/*' and '*/' in line:        
                    sample_num = int(line.split('*')[1].strip())
                    #print(sample_num)            
                    
                    if sample_num != 1:
                        weights = friendsCount_val + followersCount_val + listedCount_val + statusesCount_val                    
                        #print(id_val[:-1], weights)
                        data.append((id_val[:-1], weights))
                    continue
                
            if "ObjectId(" in line:
                    line = line.replace('ObjectId(','')
                    line = line.replace(')','')
                    lns = line.split(":")
                    _id =  lns[0].strip()
                    _id_val = lns[1].strip()[:-1].strip()
                    #print(_id,":", _id_val)
                    continue
                
            if "id" and "tag:" in line:
                    lns = line.split(":")
                    id =  lns[0].strip()
                    id_val = lns[-1].strip() [:-1].strip()
                    #print(id,":", id_val)
                    continue
                
            if "id" and "id:" in line:
                    lns = line.split(":")
                    actor_id =  lns[0].strip()
                    actor_val = lns[-1].strip()[:-1].strip()
                    #print(actor_id,":", actor_val)
                    continue
                
            if  "friendsCount" in line:
                    lns = line.split(":")
                    friendsCount =  lns[0].strip()
                    friendsCount_val = int(lns[1].strip() [:-1].strip())
                    #print(friendsCount,":", friendsCount_val)
                    continue
            if  "followersCount" in line:
                    lns = line.split(":")
                    followersCount =  lns[0].strip()
                    followersCount_val = int(lns[1].strip() [:-1].strip())
                    #print(followersCount,":", followersCount_val)
                    continue
            
            if  "listedCount" in line:
                    lns = line.split(":")
                    listedCount =  lns[0].strip()
                    listedCount_val = int(lns[1].strip() [:-1].strip())
                    #print(listedCount,":", listedCount_val)
                    continue
            
            if  "statusesCount" in line:
                    lns = line.split(":")
                    statusesCount =  lns[0].strip()
                    statusesCount_val = int(lns[1].strip() [:-1].strip())
                    #print(statusesCount,":", statusesCount_val)
                    continue
            
            if  "twitterTimeZone" in line:
                    lns = line.split(":")
                    twitterTimeZone =  lns[0].strip()
                    twitterTimeZone_val = lns[1].strip() [:-1].strip()
                    #print(twitterTimeZone,":", twitterTimeZone_val)
                    continue
                
    weights = friendsCount_val + followersCount_val + listedCount_val + statusesCount_val                    
                        #print(id_val[:-1], weights)
    data.append((id_val[:-1], weights))
    
    edg= []
    for i in range(len(data)):
        point1 = i+1
        point2 = random.randint(1,1000)
        edg.append((point1,point2))     
     
        
            
       
    for i in range(NUM_EDG):
         point1 = random.randint(1,1000)
         point2 = random.randint(1,1000)
         edg.append((point1,point2))     
     
    with open("sample_twt.txt" , "w") as f:
        pass
        
    with open("sample_twt.txt" , "a+") as f:
        for i in range(len(edg)):
            f.write(str(edg[i][0])+"   "+str(edg[i][1])+"\n")
            
    return data, edg

     
     
     