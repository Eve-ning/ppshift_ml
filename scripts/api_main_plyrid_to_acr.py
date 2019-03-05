# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 09:19:13 2019

@author: user
"""

import os
import api_main
import save_to
import time

def load_player_ids(beatmap_id: int):
    # Limit doesn't work
    player_id_f = open(save_to.dirs.dir_plyrid + str(beatmap_id) + ".plyrid", "r")
    player_id_list = [int(x) for x in player_id_f.read().splitlines()]

    return player_id_list

def get_player_replays(player_id_list: list, beatmap_id: int):
    
    replay_list = []
    status_count = 0
    status_break = 3
    
    player_id_it = 0
    
    while player_id_it < len(player_id_list):
            
        replay,status_code = api_main.get_replay(beatmap_id, 3, player_id_list[player_id_it])
        print ("BM:" + str(beatmap_id) + "\tPL:" + str(player_id_it + 1) + "/50")
        
        if (status_code == 200):
            # Reset Count on Good input
            status_count = 0
            player_id_it += 1;
            replay_list.append(replay)
        elif (status_code == 0):
            # When the replay is corrupt we append a dummy value
            replay_list.append([0, 0])
            print("Bad Replay, appending dummy value.")
            player_id_it += 1;
        else:
            # Count up Status Errors 
            status_count += 1
            # Bad GET, we will wait 3 more seconds
            print ("Bad Status: " + str(status_code))
            time.sleep(3)
            
            if (status_count == status_break):
                print ("Bad Status Threshold Exceeded")
                return None
        
    return replay_list
    
    
def run():

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
        if (save_to.exists(save_to.dirs.dir_acr, beatmap_id)):
            continue
        
        print("get: " + beatmap_id + "\t|\t" + str(files_counter) + " out of " + str(files_len))
        
        id_list = load_player_ids(int(beatmap_id))
        rpl = get_player_replays(id_list, int(beatmap_id))
        
        if (rpl == None):
            print("Program break")
            input("Enter to Exit: ")
            return
        
        save_to.diff_directory(save_to.dirs.dir_acr, rpl, beatmap_id, "acr")
  
run()          
# =============================================================================
# if (not save_to.exists(save_to.dirs.dir_acr, str(342369))):
#     id_list = load_player_ids(342369)[0:2]
#     rpl = get_player_replays(id_list, 342369)
#     save_to.diff_directory(save_to.dirs.dir_acd,rpl,str(342369),"acr")
# else:
#     print("Exists")
# =============================================================================
# =============================================================================
# print(api_main.get_replay(823842, 3, 1824775))
# =============================================================================


