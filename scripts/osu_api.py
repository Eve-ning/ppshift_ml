# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 21:52:55 2019

@author: user
"""

import requests
import time
import json

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
    
    time.sleep(6) # Pause
    
    return json_data, response.status_code
