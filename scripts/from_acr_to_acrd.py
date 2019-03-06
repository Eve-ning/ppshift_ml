# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 12:33:32 2019

@author: user
"""

import save_to
import ast

def get_deviation(acr: list, acd: list):

#    unq_acr_keys = list(set([x[1] for x in acr]))
    
    unq_acd_keys = list(set([x[1] for x in acd]))
    # remove +K
    unq_acd_keys = list(filter(lambda x: x[0] != "+", unq_acd_keys))
    unq_acd_keys = [int(x) for x in unq_acd_keys]
    
    acd = [[int(x) for x in n] for n in acd]
    
    acr_closest_list = []
    
    for key in unq_acd_keys:
        
        acr_k = list(filter(lambda x: x[1] == key, acr))
        acd_k = list(filter(lambda x: x[1] == key, acd))
        
# =============================================================================
#         print("ACR K:" + str(key) + str(acr_k))
#         print("ACD K:" + str(key) + str(acd_k))
# =============================================================================
        if (len(acr_k) != 0):
            for note in acd_k:
                acr_closest = min(acr_k, key=lambda x:abs(x[0]-note[0]))
                acr_closest_list.append(acr_closest)
            
            
    # Align both lists
    acr_closest_list.sort(key=lambda x:x[1])
    acd.sort(key=lambda x:x[1])
    
    counter = 0
    
    while (counter < len(acd)):
        dev = acd[counter][0] - acr_closest_list[counter][0]
        if (abs(dev) > 20):
            print(acd[counter][0] - acr_closest_list[counter][0], end="\t") 
        
        counter += 1
    print()
    print(len(acd))
    
# =============================================================================
#     print(acr_closest_list)
#     print(acd)
# =============================================================================
    
def load_acr(beatmap_id: int):
    
    return open(save_to.dirs.dir_acr + str(beatmap_id) + ".acr", "r").read().splitlines()
    
def load_acd(beatmap_id: int):
    
    return open(save_to.dirs.dir_acd + str(beatmap_id) + ".acd", "r").read().splitlines()


b_id = 1101044
acr = load_acr(b_id)
acd = load_acd(b_id)
acd = [x.split(",") for x in acd]

get_deviation(ast.literal_eval(acr[0]), acd)
#get_deviation(l)