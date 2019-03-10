# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 09:19:13 2019

@author: user
"""

import api_main
import save_to
import time
import get_beatmap_metadata

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
    beatmap_ids = save_to.get_beatmap_ids(save_to.dirs.dir_diff, save_to.dirs.dir_acr)
    
    # This filters out any beatmap < 5.0 SR
    filtered_ids = get_beatmap_metadata.get_id_by_filters(4.5)
    beatmap_ids = list(filter(lambda x: x in filtered_ids, beatmap_ids))

    
    id_len = len(beatmap_ids)
    id_counter = 0
    
    for beatmap_id in beatmap_ids:
        
        id_counter += 1
        print("get: " + str(beatmap_id) + "\t|\t" + str(id_counter) + " out of " + str(id_len))
        
        id_list = load_player_ids(beatmap_id)
        rpl = get_player_replays(id_list, beatmap_id)
        
        if (rpl == None):
            print("Program break")
            input("Enter to Exit: ")
            return
        
        save_to.diff_directory(save_to.dirs.dir_acr, \
                               save_to.flatten_2d_list(rpl), \
                               str(beatmap_id), "acr")
         

run()