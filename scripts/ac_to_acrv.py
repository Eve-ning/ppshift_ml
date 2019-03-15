# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 12:33:32 2019

@author: user
"""

import statistics

def run(acr: list, acd: list):
    
# =============================================================================
#     print(acr[0][0:100])
#     print(acd[0:100])
# =============================================================================
    
    # We find the unique keys from the map
    # We will then loop over the keys to find all deviations
    unq_acd_keys = list(set([x[1] for x in acd]))
    
    # We skip + because replays don't specify + on LN or + on NN
    unq_acd_keys = list(filter(lambda x: x[0] != "+", unq_acd_keys))
    
    # Convert all to int
    unq_acd_keys = [int(x) for x in unq_acd_keys]
    
    # Convert all to int to allow arithmetic
    acd_int = [[int(x) for x in n] for n in acd]
    
    # Output in dictionary
    deviation_dic = {}

    for replay in acr:
        
        # Skip all dummies
        if (len(replay) < 10):
            continue
        
        # This will specify all objects that meet the criteria of being closest
        # to the acd
        acr_closest_list = []
        
        # Loop through by each key
        for key in unq_acd_keys:
            
            # Get only the actions that correspond to the key
            acr_k = list(filter(lambda x: x[1] == key, replay))
            acd_k = list(filter(lambda x: x[1] == key, acd_int))
            
            # print ("KEY: " + str(key))
            # print ("ACR: " + str(len(acr_k)))
            # print ("ACD: " + str(len(acd_k)))
            # This will occur if the map doesn't have LNs on a column
            # Eg. -3 will not occur if LNs don't appear on col3
            if (len(acr_k) != 0):
                for note in acd_k:
                    # This gets the item that has the minimum abs difference
                    acr_closest_list.append(
                            min(acr_k, key=lambda x:abs(x[0]-note[0])))
                
                
        
        # Align both lists
        acr_closest_list.sort(key=lambda x:x[1])
        acd.sort(key=lambda x:int(x[1]))
        
        # If lengths are different, we will have an issue
        if (len(acd) != len(acr_closest_list)):
            print("Bad Length")
            return
        
        # Count through the whole list
        # Indexes should be consistent between the 2 lists
        counter = 0
        
        while (counter < len(acd)):
            offset_d = int(acd[counter][0])
            offset_r = acr_closest_list[counter][0]
            key = acd[counter][1]
            dev = offset_d - offset_r
             
            # We set the default to be a blank array
            deviation_dic.setdefault((offset_d, key),[])
            
            # Append dev to the key
            deviation_dic[(offset_d, key)].append(dev)

            counter += 1
    
    deviation_dic = get_deviation_median(deviation_dic)
    
    # Flatten the dictionary to a list
    deviation_l = []
    
    for dev_k, dev_v in deviation_dic.items():
        # print(dev_k)
        # print(dev_v)
        deviation_l.append([dev_k[0], dev_k[1], dev_v[0]])
    
    # Sort by offset
    deviation_l.sort(key=lambda x : x[0])
    
    # For each offset, we only want 1 output, so we will groupby and aggregate
    # by mean
    deviation_l_grouped = []
    offset_buffer = deviation_l[0][0]
    median_sum = 0
    counter = 0
    
    deviation_l.append([99999999,9,0])
    for dev in deviation_l:
        
        # If it's the same as the buffer, we will add onto the median
        if (offset_buffer == dev[0]):
           median_sum += dev[2] 
           counter += 1
           
        else: # Not the same, new entry
            # We will append the previous entry
            deviation_l_grouped.append([offset_buffer, median_sum/counter])
            # Reset all parameters
            offset_buffer = dev[0]
            median_sum = dev[2]
            counter = 1
    
    return (deviation_l_grouped)

def get_deviation_median(deviation: dict):
    
    for k, x in deviation.items():
        dev_abs = [abs(d) for d in x]
        deviation[k] = [statistics.median(dev_abs)]
        
    return deviation
    
    
    
    
