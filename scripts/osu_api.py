# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 21:52:55 2019

@author: user
"""

import requests
import time
import json
import base64
import lzma
import operator

# GLOBAL VAR
base_api_url = "https://osu.ppy.sh/api/"
api_key_url = open("D:\\Data Documents\\auth\\osu_api_key.txt", "r")
api_key = api_key_url.readline()
api_key_url.close()

def get_scores(beatmap_id: int, mode: int, limit: int):
    param = {
            "k": str(api_key),
            "b": beatmap_id,
            "m": mode,
            "l": limit
            }
    api_url = base_api_url + "get_scores"
    response = requests.get(api_url, params = param)
    json_data = json.loads(response.text)
    
    time.sleep(1) # Pause
    
    return json_data, response.status_code

def get_replay(beatmap_id: int, mode: int, user: int):
    param = {
            "k": str(api_key),
            "b": beatmap_id,
            "m": mode,
            "u": user
            }
    api_url = base_api_url + "get_replay"
    response = requests.get(api_url, params = param)
    json_data = json.loads(response.text)
    
    # We will decode the content here
    # But we check the status code before proceeding
    time.sleep(6) # Pause
    
    # If response is not 200
    if (response.status_code != 200):
        return "bad request", response.status_code
    
    decoded = base64.b64decode(json_data["content"])
    decompressed = str(lzma.decompress(decoded))[:-2]
    decompressed = decompressed[2:]
    
    # We split it into a nested list
    output = [x.split("|") for x in decompressed.split(",")]
    
    # Drop the last 2 useless elements    
    [x.pop(2) for x in output]
    [x.pop(2) for x in output]
    
    return convert_replay_data(output), response.status_code

def convert_replay_data(replay_data: list):
    
    # Eg. 1 3 4 (bin: 25) will output
    # [1,0,1,1,0,0,0,0,0]   
    def decode_key_action(action: int):
        
        # Convert action to string List
        action_str = list(bin(action)[:1:-1])
        
        # Find how many missing elements and append them
        action_missing = 9 - len(action_str)
        action_str.extend(['0'] * action_missing)
        
        # Convert string List to int List
        action_int = list(map(int, action_str))
        
        # Add the list together to ensure 9 element cases
        return action_int
    
    # [0,0,1,0,0,1,0,0,0] prev
    # [0,1,0,0,0,1,0,0,0] curr
    # [0,1,-1,0,0,0,0,0,0] output
    def get_action_difference(prev_flag: list, curr_flag: list):
        
        # Gets the difference between curr and prev
        diff_flag = list(map(operator.sub, curr_flag, prev_flag))
        
        # 1:  1 - 0 <Key Pressed>
        # 0:  0 - 0 | 1 - 1 <No Change>
        # -1: 0 - 1 <Key Released>
        
#        print('prev: {}'.format(prev_flag))
#        print('curr: {}'.format(curr_flag))
#        print('diff: {}'.format(diff_flag))
        
        # We are required to + 1 as -0 and +0 are the same
        # So columns will always start from 1 to 9
        key_p = [(i + 1) for i, y in enumerate(diff_flag) if y == 1]
        key_r = [-(i + 1) for i, y in enumerate(diff_flag) if y == -1]
        
        output = []
        output.extend(key_p)
        output.extend(key_r)
        return output
            
    timestamp = 0
    prev_action = [0] * 9
    curr_action = [0] * 9
    
    output = []
    
    for step in replay_data:

        timestamp += int(step[0])
        
        curr_action = decode_key_action(int(step[1]))
        diff_action = get_action_difference(prev_action, curr_action)
        
        # Skip if there's no change in action
        if (len(diff_action) == 0):
#            print('--skip--')
            continue
#        print ('diff: {}'.format(diff_action))
        # For each key press/release, we append to output as a separate action
        if (timestamp > 0):
            for key in diff_action:
                output.append([timestamp, key])
                
        prev_action = curr_action
  
#    print('otpt: {}'.format(output))
    return output


# Granat - Drop, Player: GH_CHAIKA
# Map: https://osu.ppy.sh/beatmapsets/281349#mania/647965
#cont, code = get_replay(647965, 3, 2462317)
#
#print(cont)


