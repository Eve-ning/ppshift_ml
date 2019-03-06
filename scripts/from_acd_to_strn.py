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
weight_ssh = 0.25
weight_ssb = 0.1
strain_decay_per_s = 1
strain_decay_perc_per_s = 75

# =============================================================================
# beatmap_ids = {(1001780, 'ETERNAL DRAIN - Eternal'),
#                (1104774, 'ETERNAL DRAIN - Black Another'),
#                (1002502, 'ETERNAL DRAIN - Another')}
# =============================================================================


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
                
        # Calculate reading difficulty here!
        reading_val = (nn_count + (lnh_count + lnt_count) * gamma)/theta
        counts_l.append([x, nn_count, lnh_count, lnt_count, reading_val])
        
    acd = pandas.DataFrame(counts_l, columns = ['offset', 'nn_count', 'lnh_count', 'lnt_count', 'reading_val'])
    
    return acd
    
def get_weights(acd: pandas.DataFrame) -> pandas.DataFrame:
    
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

for beatmap_id in beatmap_ids:
    acd = pandas.DataFrame(get_acd(beatmap_id[0]), columns = ['offset', 'key'])
    plot = get_strain(get_weights(acd)).plot(x='offset', title=beatmap_id[1]).get_figure()
    plot.savefig(str(beatmap_id))




# =============================================================================
# get_weights(acd)   
# =============================================================================
# =============================================================================
# print(get_reading(acd))
# =============================================================================

# =============================================================================
# ts = pandas.Series(numpy.random.randn(1000),index=pandas.date_range('1/1/2000', periods=1000))
# ts = ts.cumsum()
# ts.plot()
# =============================================================================
