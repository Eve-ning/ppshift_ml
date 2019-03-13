# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 18:32:15 2019

@author: user
"""

import pandas
import save_to
import os
import get_beatmap_metadata

# Output
# Offset, Reading, Strain

# HYPERPARAMETERS
theta = 1000
gamma = 0.75
sigma = 2
weight_nn = 1
weight_lnh = 0.75
weight_lnt = 0.75
weight_ssh = 0.25
weight_ssb = 0.1
strain_decay_per_s = 5
strain_decay_perc_per_s = 75



# This represents the distribution from the keys to the fingers
# 4: [LM][LI][RI][RM]
# 5: [LM][LI][S][RI][RM]
# 6: [LR][LM][LI][RI][RM][RR]
# 7: [LR][LM][LI][S][RI][RM][RR]
# 8: [LP][LR][LM][LI][RI][RM][RR][RP]
# 9: [LP][LR][LM][LI][S][RI][RM][RR][RP]


def get_acd(beatmap_id: int) -> pandas.DataFrame:
    f = [x.split(",") for x in open(save_to.dirs.dir_acd + str(beatmap_id) + ".acd").read().splitlines()]
    f = list(map(lambda x: [int(x[0]),x[1]], f))
    return f

def get_reading(acd: pandas.DataFrame) -> pandas.DataFrame:
        
    # Unique offset
    unq_offset = acd['offset'].unique()
    
    counts_l = []
    
    # For each unique offset
    for x in unq_offset:
        # We get the Series that includes all notes that is within the range
        # x - theta <= note <= x + theta
        search = acd[(x <= acd['offset']) & (x + theta >= acd['offset'])]
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
                
#        reading_val = (nn_count + (lnh_count + lnt_count) * gamma)/theta
        counts_l.append([x, nn_count, lnh_count, lnt_count])
                
    acd = pandas.DataFrame(counts_l, columns = ['offset', 'nn_count', 'lnh_count', 'lnt_count'])
    
    return acd
    
def get_weights(acd: pandas.DataFrame) -> pandas.DataFrame:
    
    weights_l = []
    
    # We group by offset
    acd_offset_grp = acd.groupby(['offset'])
    
    # For each offset, we grab the DF
    for offset, grp in acd_offset_grp:
        
        offset_r = [offset, 0,0,0,0,0,0,0,0,0] # Get an empty offset row
        
        # For each key in that offset, we look at the key distribution
        # We will assign that key according to that distribution
        for k in grp['key']:  
            
            # We will find out what weight we are using on the key
            weight = 0
            if (k[0].isdigit()):
                weight = weight_nn
            elif (k[0] == '-'):
                weight = weight_lnt
            elif (k[0] == '+'):
                weight = weight_lnh
            else:
                raise 
            
            k = abs(int(k)) # We don't need the details of the string anymore
            
            # Even though the list doesn't start key first, the key is already
            # offset by + 1, so we don't need to adjust the index
            offset_r[k] += weight
            
            # We will firstly calculate the weight that is transferred to
            # The other fingers on the hand (Denoted by Strain Shift Hand)
            weight_h = weight * weight_ssh
            # The other hand (Denoted by Strain Shift Body)
            weight_b = weight * weight_ssb
            
            # The list excluded, we will get the SS weights
            other_k = list(range(1,10)) # [1,2,...,8,9]
            other_k.pop(k - 1) # Due to indexing, we need to -1
            
            for other_k_ea in other_k:
                # If they are on the same hand, we add calculated WEIGHT_H
                if ((k < 5 and other_k_ea < 5) or \
                    (k >= 5 and other_k_ea >= 5)):
                    offset_r[other_k_ea] += weight_h
                # If they are on the same body, we add calculated WEIGHT_B
                else:
                    offset_r[other_k_ea] += weight_b
                
        # Push the weights to the list
        weights_l.append(offset_r)
            
    weights = pandas.DataFrame(weights_l,\
        columns = ['offset', 'LP','LR','LM','LI','S','RI','RM','RR','RP'])
    
    return weights

def get_strain(weight_df: pandas.DataFrame):
    
    key_column_names = list(weight_df.columns.values)[1:]
    strain_key_column_names = [(x + "_S") for x in key_column_names[1:]]
    key_column_names.extend(strain_key_column_names)
    
    strain_df = pandas.DataFrame(weight_df['offset'])
    
    # We will loop through all the 9 keys
    for k in range(0,9):
        key_column_name = key_column_names[k]

        strain_l = []
        
        offset_prev = 0
        strain_prev = 0
        strain = 0
        
        for offset, weight in weight_df[["offset",key_column_name]].itertuples(index=False):
            elapsed_s = (offset - offset_prev)/1000
            
            strain = (strain_prev * ((strain_decay_perc_per_s/100) ** (elapsed_s))) - (elapsed_s * strain_decay_per_s)
            # strain will never go below 0
            strain = 0 if strain < 0 else strain
            # We add the weight AFTER the decay
            strain += weight
            
            strain_l.append([offset, strain])
            
            strain_prev = strain
            offset_prev = offset
            
        strain_k_df = pandas.DataFrame(strain_l, columns = ['offset', key_column_name])
        strain_df = pandas.merge(strain_df, strain_k_df, how='inner', on=['offset','offset'])
        
    return strain_df

def get_replay(beatmap_id: int):
    
    f = [x.split(',') for x in open(save_to.dirs.dir_acrv + str(beatmap_id) + '.acrv', "r").read().splitlines()]

    replay_df = pandas.DataFrame(f, columns=['offset','key','median','mean','variance'])
    
    replay_df.drop(replay_df.columns[[1,3,4]], axis=1, inplace=True)

    replay_df = replay_df.apply(pandas.to_numeric)
    replay_df = replay_df.sort_values(by='offset')

    # We replace median with a rolling mean of a 30 window
    replay_df['roll'] = replay_df['median'].rolling(window=30).mean()
    replay_df = replay_df.drop(['median'], axis=1)
    # Due to rolling, we need to clean the NaNs with 0
    replay_df = replay_df.fillna(0)

    return replay_df

    
def run(acd: list, acrv: list):
        
    # Grab ACD
    acd_df = pandas.DataFrame(acd, columns = ['offset', 'key'])
    
    # Get strain via weight
    strain = get_strain(get_weights(acd_df))
    
    # Get reading
    reading = get_reading(acd_df)
    
    print(strain)
    print(reading)

    # strain + reading Merge
    df = pandas.merge(strain, reading, how='inner', on=['offset'])

    # strain + reading + replay (last col)
    df = pandas.merge(df, acrv, how='inner', on=['offset'])  
    
    df = df.apply(pandas.to_numeric)
    return df
        
