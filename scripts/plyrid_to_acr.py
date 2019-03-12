# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 09:19:13 2019

@author: user
"""

import api_main
import time
import osuho_to_acd

def run(player_id_list: list, beatmap_id: int, keys: int):
    
    replay_list = []
    status_count = 0
    status_break = 3
    
    player_id_it = 0
    
    while player_id_it < len(player_id_list):
            
        replay,status_code = api_main.get_replay(beatmap_id, 3, player_id_list[player_id_it])
        print ("BM:" + str(beatmap_id) + "\tPL:" + str(player_id_it + 1) + "/50")
        
        if (status_code == 200):
            # We will need to convert all columns to actions
            replay_n = []
            
            for pair in replay:
                
                offset = pair[0]
                column = pair[1]
                
                # This is required as we cannot convert with a negative column
                is_release = column < 0 
                action = osuho_to_acd.column_to_action[keys][abs(column) - 1]
                action = -action if is_release else action
                
                replay_n.append([offset, action])
            
            # Reset Count on Good input
            status_count = 0
            player_id_it += 1
            replay_list.append(replay_n)
            
        elif (status_code == 0):
            # When the replay is corrupt we append a dummy value
            replay_list.append([0, 0])
            print("Bad Replay, appending dummy value.")
            player_id_it += 1
            
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
        
        

print(run([6659363],1104774,4))