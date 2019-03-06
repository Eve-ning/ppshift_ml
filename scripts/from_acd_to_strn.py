# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 18:32:15 2019

@author: user
"""

import pandas
import save_to

# Output
# Offset, Reading, Strain

# HYPERPARAMETERS
theta = 1000
gamma = 0.75
sigma = 2
weight_nn = 1
weight_lnh = 0.75
weight_lnt = 0.75
weight_ssh = 0.1
weight_ssb = 0.02

# This represents the distribution from the keys to the fingers
# 4: [LM][LI][RI][RM]
# 5: [LM][LI][S][RI][RM]
# 6: [LR][LM][LI][RI][RM][RR]
# 7: [LR][LM][LI][S][RI][RM][RR]
# 8: [LP][LR][LM][LI][RI][RM][RR][RP]
# 9: [LP][LR][LM][LI][S][RI][RM][RR][RP]
key_distr_dict = {
        4: [2,3,5,6],
        5: [2,3,4,5,6],
        6: [1,2,3,5,6,7],
        7: [1,2,3,4,5,6,7],
        8: [0,1,2,3,5,6,7,8],
        9: [0,1,2,3,4,5,6,7,8],
        }

def get_acd(beatmap_id: int) -> pandas.DataFrame:
    f = [x.split(",") for x in open(save_to.dirs.dir_acd + str(beatmap_id) + ".acd").read().splitlines()]
    f = list(map(lambda x: [int(x[0]),x[1]], f))
    return f

def get_reading(acd: pandas.DataFrame):
        
    # Unique offset
    unq_offset = acd['offset'].unique()
    
    counts_l = []
    
    for x in unq_offset:
        search = acd[(x - theta <= acd['offset']) & (x + theta >= acd['offset'])]
        nn_count = 0
        lnh_count = 0
        lnt_count = 0
        for k in search['key']:
            if (k[0].isdigit()):
                nn_count += 1
            elif (k[0] == '+'):
                lnh_count += 1
            else: 
                lnt_count += 1
                
        # Calculate reading difficulty here!
        reading_val = (nn_count + (lnh_count + lnt_count) * gamma)/theta
        counts_l.append([x, nn_count, lnh_count, lnt_count, reading_val])
        
    counts = pandas.DataFrame(counts_l, columns = ['offset', 'nn_count', 'lnh_count', 'lnt_count', 'reading_val'])
    
    acd = pandas.merge(acd, counts, how='inner', on = ['offset','offset'])
    
    return acd
    
def get_weights(acd: pandas.DataFrame):
    
    weights_l = []
    
    # Get the key count, we can get it by looking at the maximum key
    key_max = acd['key'].max()
    key_distr = key_distr_dict[int(key_max)] # We use that to get the correct distr

    # We group by offset
    acd_offset_grp = acd.groupby(['offset'])
    
    # For each offset, we grab the DF
    for offset, grp in acd_offset_grp:
        
        offset_r = [offset, 0,0,0,0,0,0,0,0,0] # Get an empty offset row
        
        # For each key in that offset, we look at the key distribution
        # We will assign that key according to that distribution
        for k in grp['key']:  
            
            # The index of key_distr
            curr_distr_index = key_distr[abs(int(k)) - 1]
            # L if left hand, R if right hand
            curr_distr_hand = 'L' if curr_distr_index < 4 else 'R'
            # Assign weight
            offset_r[curr_distr_index + 1] += weight_nn
            
            # The list excluded, we will get the SS weights
            excl_distr_index = list(filter(lambda x: x != curr_distr_index, key_distr))
            
            for excl_index in excl_distr_index:
                # If they are on the same hand, we add SSH
                if ((curr_distr_hand == 'L' and excl_index < 4) or \
                    (curr_distr_hand == 'R' and excl_index >= 4)):
                    offset_r[excl_index + 1] += weight_ssh
                # If they are on the same body, we add SSB
                else:
                    offset_r[excl_index + 1] += weight_ssb
                
        # Push the weights to the list
        weights_l.append(offset_r)
            
    weights = pandas.DataFrame(weights_l,\
        columns = ['offset', '[LP]','[LR]','[LM]','[LI]','[S]','[RI]','[RM]','[RR]','[RP]'])
    
    print(weights)

        
def get_strain(weights: list):
    
    print()
    
acd = pandas.DataFrame(get_acd(690909), columns = ['offset', 'key'])

get_weights(acd)   
    

