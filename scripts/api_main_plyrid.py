# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 09:19:13 2019

@author: user
"""

import api_main
import save_to

def get_player_ids(beatmap_id: int):
    # Limit doesn't work
    score_list, status_code = api_main.get_scores(beatmap_id, 3, 50)
    if (status_code != 200):
        return None;    
    
    id_list = [x['user_id'] for x in score_list]
    return id_list
    
def run():

    beatmap_ids = save_to.get_beatmap_ids(save_to.dirs.dir_osuho, save_to.dirs.dir_acd)
    id_len = len(beatmap_ids)
    id_counter = 0
    
    for beatmap_id in beatmap_ids:
        id_counter += 1
        
        print("get: " + beatmap_id + "\t|\t" + str(id_counter) + " out of " + str(id_len))
        
        id_list = get_player_ids(beatmap_id)
        
        if (id_list == None):
            print("Skipped on error: " + beatmap_id)
            continue;
        
        save_to.diff_directory(save_to.dirs.dir_plyrid, \
                               id_list,str(beatmap_id),"plyrid",False)
        
run()


