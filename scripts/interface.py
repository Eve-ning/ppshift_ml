# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 18:06:45 2019

@author: user
"""

import interface_class
import api_main


beatmap_info_path = \
"D:\\Data Documents\\ppshift\\ppshift_ml\\documents\\beatmap_info\\beatmap_info.txt"

# This is where we use interface_class

def download_beatmap_info(YYYYMMDD: str, until_YYYYMMDD: str):
    
    data = api_main.get_beatmaps_since_ext(YYYYMMDD, until_YYYYMMDD)
    f = open(beatmap_info_path, "w+", encoding="utf-8")
    f.write(str(data))
        
    return

def load_beatmap_info():
    
    f = open(beatmap_info_path, "r", encoding="utf-8")
    return eval(f.read())

def get_ids(star_rating_below = None,
            star_rating_above = None,
            
            ):
    
    
    return