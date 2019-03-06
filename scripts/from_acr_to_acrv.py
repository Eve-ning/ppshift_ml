# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 12:33:32 2019

@author: user
"""

import save_to
import os
import ast
import statistics

def get_deviation(acr: list, acd: list):

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
        
        # This will specify all objects that meet the criteria of being closest
        # to the acd
        acr_closest_list = []
        
        # Loop through by each key
        for key in unq_acd_keys:
            
            # Get only the actions that correspond to the key
            acr_k = list(filter(lambda x: x[1] == key, replay))
            acd_k = list(filter(lambda x: x[1] == key, acd_int))
            
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
             
    return (deviation_dic)

def get_deviation_median(deviation: dict):
    
    for k, x in deviation.items():
        dev_abs = [abs(d) for d in x]
        deviation[k] = [
                statistics.median(dev_abs),
                statistics.mean(dev_abs),
                statistics.variance(dev_abs)]
        
    return deviation

def load_acr(beatmap_id: int):
    
    f = open(save_to.dirs.dir_acr + str(beatmap_id) + ".acr", "r"
             ).read().splitlines()
    f = list(filter(lambda x: x != "0,0", f)) # This is to remove all dummies
    return([ast.literal_eval(x) for x in f])
    
def load_acd(beatmap_id: int):
    
    f = open(save_to.dirs.dir_acd + str(beatmap_id) + ".acd", "r"
             ).read().splitlines()
    return [x.split(",") for x in f]

def run():

      # Get all diff id from the dir
    files = os.listdir(save_to.dirs.dir_acr)
    files_len = len(files)
    files_counter = 0
    
    for f in files:
        files_counter += 1
        
        # Skip non .osu files
        if (not "." in f):
            continue
        
        # Extract Ids
        beatmap_id = str(f.split(".")[0])
        
        # Skip if exist
        if (save_to.exists(save_to.dirs.dir_acrv, beatmap_id)):
            continue
        
        print("get: " + beatmap_id + "\t|\t" + str(files_counter) + " out of " + str(files_len))
            
        acr = load_acr(int(beatmap_id))
        acd = load_acd(int(beatmap_id))
        
        dev_med = get_deviation_median(get_deviation(acr, acd))
        dev_med_as_list = []
        
        # Convert Dict to List
        for k, x in dev_med.items():
            dev_med_as_list.append([k[0], k[1], x[0], x[1], x[2]])

        save_to.diff_directory(save_to.dirs.dir_acrv, dev_med_as_list, beatmap_id, "acrv")

run()
