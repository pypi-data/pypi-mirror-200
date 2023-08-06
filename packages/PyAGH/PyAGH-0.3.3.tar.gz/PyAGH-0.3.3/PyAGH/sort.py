import pandas as pd

def sortPed(data):
    '''Sort pedigree by birthdate.

    data: the pedigree data with 3 columns(id,sire,dam) in dataframe type.
    '''
    if not isinstance(data, pd.DataFrame): ###must data.frame
        print("Please provide data with dataframe type!")
        return
    if data.shape[0] == 0:
        print("data is null!")
        return
    if data.shape[1] != 3:
        print("Data must have three columns, please verify")
        return
    if data.iloc[:,0].shape[0] != data.iloc[:,1].shape[0]:
        print("ID has to be of the same length than sire and dam")
        return
    if data.iloc[:,2].shape[0] != data.iloc[:,1].shape[0]:
        print("sire and dam have to be of the same length")
        return
    ###The missing values in the input data are NA and 0. If NA exists, it will be converted to 0
    data.fillna(0)
    ###Remove completely duplicate rows
    data = data.astype(str)
    data = data[~data.duplicated()]

    if any(data.iloc[:,0].duplicated()): ##Check for errors where the same individuals exist but the parents are not the same, that is, there are only duplicates in the individual column
        print("some individuals appear more than once in the pedigree")
        return
    ###Check if all parents are 0
    if all(data.iloc[:,1] =="0") and all(data.iloc[:,2]=="0"):
        print("All dams and sires are missing")
        return
    ##Check for errors where individuals appear in both the father and mother columns
    if any(data[data.iloc[:,1] != "0"].iloc[:,1].isin(data[data.iloc[:,1] != "0"].iloc[:,2])):
        print("Dams appearing as Sires")
        return
    ###Check whether an individual is their own parent
    if any(data.iloc[:,0] == data.iloc[:,1]) or any(data.iloc[:,0] == data.iloc[:,2]):
        print("Individual appearing as its own Sire or Dam")
        return
    
    tmp = pd.concat([data.iloc[:,1],(data.iloc[:,2])]).drop_duplicates().astype(str)
    tmp = tmp.reset_index(drop=True)
    tmp.drop(tmp[tmp == "0"].index,inplace=True) #missing value is 0
    index = ~tmp.isin(data.iloc[:,0].astype(str))
    missingP =pd.Series(dtype=str)
    if any(index):
        missingP = tmp[index]
        lable01 = pd.concat([missingP,data.iloc[:,0]]).reset_index(drop=True)  
        sire01 = pd.concat([pd.Series(["0"]*len(missingP)),data.iloc[:,1]]).reset_index(drop=True)
        dam01 = pd.concat([pd.Series(["0"]*len(missingP)),data.iloc[:,2]]).reset_index(drop=True)
    else:
        lable01 = pd.concat([data.iloc[:,0]]).reset_index(drop=True)  
        sire01 = pd.concat([data.iloc[:,1]]).reset_index(drop=True)
        dam01 = pd.concat([data.iloc[:,2]]).reset_index(drop=True)
    sire = pd.Categorical(sire01,categories=lable01).codes
    dam = pd.Categorical(dam01,categories=lable01).codes
    nped = len(lable01)
    lable = pd.Series(range(nped))
    sire = pd.Series(sire)
    dam = pd.Series(dam)
    
    pede = pd.DataFrame({"id":lable,
                        "sire":sire,
                        "dam":dam,
                        "gene_p1": None,
                        "gene_p2":None,
                        "gene_max":None,
                        })
    noParents=(pede["sire"] == -1) & (pede["dam"] == -1)
    pede.loc[noParents,"gene_p1"] = 0
    pede.loc[noParents,"gene_p2"] = 0
    pede.loc[noParents,"gene_max"] = 0
    pede = pede.to_dict()
    
    global flag
    flag = True
    global count
    for i in range(nped):
        if flag:
            if pede["gene_p1"][i] == None:
                count = 0
                pede = getGenAncestors(pede,i)
        else:
            break
    if flag:    
        ans = pd.DataFrame({"id":lable01,
                    "sire":sire01,
                    "dam":dam01,
                    "gene_max":pd.Series(pede["gene_max"]),
                    "gene_p1":pd.Series(pede["gene_p1"]),
                    "gene_p2":pd.Series(pede["gene_p2"])
                    })
        ans['gene_min'] = ans[['gene_p1','gene_p2']].min(axis=1)
        ans.sort_values(["gene_max","gene_min"],inplace=True,ascending=[True,True])
        ans.reset_index(inplace=True,drop=True)
        return ans.iloc[:,0:3]
    else:
        print("ERROR: infinite pedigree loop involving individual")
        print("The first error individual is %s" % lable01[i-1])

def getGenAncestors(pede,i):
 
    global flag
    global count
    count += 1
 
    if count < 100:
        sire = pede["sire"][i]
        dam = pede["dam"][i]

        if sire != -1:
            tmpgenP1 = pede["gene_max"][sire]
            if tmpgenP1 == None:

                pede = getGenAncestors(pede,sire)
                genP1 = 1+ pede["gene_max"][sire]
            else:
                
                genP1 = 1 + tmpgenP1
        else:
            genP1 = 0
        if dam != -1:
            tmpgenP2 =pede["gene_max"][dam]
            if tmpgenP2 == None:
                
                pede = getGenAncestors(pede ,dam)
                genP2 = 1+ pede["gene_max"][dam]
                
            else:
                genP2 = 1+tmpgenP2
        else:
            genP2 = 0
        pede["gene_max"][i] = max(genP1,genP2) 
        pede["gene_p1"][i] = genP1
        pede["gene_p2"][i] = genP2 
        return pede
     
    else:
        print("infinite pedigree loop involving individual")
        flag = False
        return 

