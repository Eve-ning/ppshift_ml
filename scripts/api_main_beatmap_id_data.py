# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 17:44:36 2019

@author: user
"""

import os
import save_to
import api_main
import time

def get_arcv_data():
    files = os.listdir(save_to.dirs.dir_acrv)
    metadata_l = []
    
    for x in files:
        beatmap_id = int(x.split(".")[0])
        
        # I understand it's ugly
        print("Get: " + x)
        content, status = api_main.get_beatmap(beatmap_id)
        if (status != 200):
            print("Bad Status: " + str(status) + ", Wait for 2 seconds before retrying...")
            time.sleep(2)
            content, status = api_main.get_beatmap(beatmap_id)
            if (status != 200):
                print("Bad Status: " + str(status) + ", Wait for 10 seconds before retrying...")
                time.sleep(10)
                content, status = api_main.get_beatmap(beatmap_id)
                if (status != 200): 
                    print("Bad Status Threshold Reached.")
                    return 0;
                
        metadata = str(beatmap_id) + "\t" + \
                   content[0]["difficultyrating"] + "\t" + \
                   content[0]["artist"] + "\t" + \
                   content[0]["title"] + "\t" + \
                   content[0]["version"] + "\t" + \
                   content[0]["creator"]
        metadata_l.append(metadata)     
        
        
    save_to.diff_directory(save_to.dirs.dir_doc, metadata_l, "arcv_metadata", "txt", False)
    
get_arcv_data()