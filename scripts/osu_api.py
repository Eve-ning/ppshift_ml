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

# GLOBAL VAR
base_api_url = "https://osu.ppy.sh/api/"
api_key_url = open("D:\\Data Documents\\auth\\osu_api_key.txt", "r")
api_key = api_key_url.readline()

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
    
    # We split it into a nested list
    output = [x.split("|") for x in decompressed.split(",")]
    
    # Drop the last 2 useless elements    
    [x.pop(2) for x in output]
    [x.pop(2) for x in output]
    
    return output, response.status_code

#cont, code = get_replay(1837187, 3, 2193881)
#
#print(code)
#print(cont)
