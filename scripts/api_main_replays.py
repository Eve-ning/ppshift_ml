# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 09:19:13 2019

@author: user
"""

import api_main
import os
import save_to

def get_player_ids(beatmap_id: int):
    # Limit doesn't work
    score_list, status_code = api_main.get_scores(beatmap_id, 3, 50)
    if (status_code != 200):
        return None;    
    
    id_list = [x['user_id'] for x in score_list]
    return id_list
    
def main():

    # Get all diff id from the dir
    files = os.listdir(save_to.dirs.dir_acd)
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
        if (save_to.exists(save_to.dirs.dir_plyrid, beatmap_id)):
            continue
        
        print("get: " + beatmap_id + "\t|\t" + str(files_counter) + " out of " + str(files_len))
        
        id_list = get_player_ids(beatmap_id)
        if (id_list == None):
            print("Skipped on error: " + beatmap_id)
            continue;
        
        save_to.diff_directory(save_to.dirs.dir_plyrid,id_list,beatmap_id,"plyrid",False)
        
if __name__== "__main__":
    main()
# =============================================================================
# print(api_main.get_replay(823842, 3, 1824775))
# =============================================================================


