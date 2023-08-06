import pandas as pd
from .sort import sortPed

def selectPed(data,id,generation=3):###Missing values are represented by 0
    '''Select pedigree.

    data: the whole pedigree with dataframe type.
    id: a list containing id which want to be selected.
    generation: int value.  Default value is 3. 
    '''
    if not isinstance(id, list): ###must list
        print("Please provide id with list type!")
        return
    if not isinstance(generation, int):
        print("ERROR: Parameter generation should be int type!")
        return
    if  generation <=0:
        print("ERROR: Parameter generation should be much than 0")
        return
    ped_ord = sortPed(data)
    
    ###Judge whether the individuals provided in the ID are all in the ped
    id = pd.Series(id).astype(str)
    if not all(id.isin(ped_ord['id'])):
        print("ERROR: there are some id not in the pedigree.")
        return
    i = 1
    ped_select = pd.DataFrame({'id':[],'sire':[],'dam':[]})
    ped_select =pd.concat([ped_select,ped_ord[ped_ord['id'].isin(id)]])
    while i < generation:
        
        i += 1

        id = pd.concat([ped_select['sire'],ped_select['dam']])
        id = id.drop_duplicates()
        id = id[id != '0']
        ped_select = pd.concat([ped_select,ped_ord[ped_ord['id'].isin(id)]])
        ped_select.drop_duplicates(inplace=True)
    
    ped_select = sortPed(ped_select)
    #print(ped_select)
    return ped_select