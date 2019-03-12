# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 12:33:32 2019

@author: user
"""

import save_to
import ast
import statistics
import pandas

def get_deviation(acr: pandas.DataFrame, acd: pandas.DataFrame):

    # We find the unique keys from the map
    # We will then loop over the keys to find all deviations
    unq_acd_actions = list(pandas.to_numeric(acd['action']).unique().values)
    
    acd_action_grp = acd.groupby(by='action')
    acr_action_grp = acr.groupby(by=['player_id', 'action'])
    
    for acr_player_name, acr_player_grp_ea in acr_player_grp:
        acr_player_grp_ea.groupby(by='action')
    
    
    # Output in dictionary
    deviation_dic = {}

    # We group by the players
    # acr_player_grp = acr.groupby(by='player_id')

    # for replay in acr:
        
    #     # This will specify all objects that meet the criteria of being closest
    #     # to the acd
    #     acr_closest_list = []
        
    #     # Loop through by each key
    #     for key in unq_acd_actions:
    
    #         # Get only the actions that correspond to the key
    #         acr_k = list(filter(lambda x: x[1] == key, replay))
    #         acd_k = list(filter(lambda x: x[1] == key, acd_int))
            
    #         # This will occur if the map doesn't have LNs on a column
    #         # Eg. -3 will not occur if LNs don't appear on col3
    #         if (len(acr_k) != 0):
    #             for note in acd_k:
    #                 # This gets the item that has the minimum abs difference
    #                 acr_closest_list.append(
    #                         min(acr_k, key=lambda x:abs(x[0]-note[0])))
                
                
    #     # Align both lists
    #     acr_closest_list.sort(key=lambda x:x[1])
    #     acd.sort(key=lambda x:int(x[1]))
        
    #     # If lengths are different, we will have an issue
    #     if (len(acd) != len(acr_closest_list)):
    #         print("Bad Length")
    #         return
        
    #     # Count through the whole list
    #     # Indexes should be consistent between the 2 lists
    #     counter = 0
        
    #     while (counter < len(acd)):
    #         offset_d = int(acd[counter][0])
    #         offset_r = acr_closest_list[counter][0]
    #         key = acd[counter][1]
    #         dev = offset_d - offset_r
             
    #         # We set the default to be a blank array
    #         deviation_dic.setdefault((offset_d, key),[])
            
    #         # Append dev to the key
    #         deviation_dic[(offset_d, key)].append(dev)

    #         counter += 1
             
    # # return (deviation_dic)

def get_deviation_median(deviation: dict):
    
    for k, x in deviation.items():
        dev_abs = [abs(d) for d in x]
        deviation[k] = [
                statistics.median(dev_abs),
                statistics.mean(dev_abs),
                statistics.variance(dev_abs)]
        
    return deviation


    
    
    
    
