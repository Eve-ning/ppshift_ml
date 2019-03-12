# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 09:19:13 2019

@author: user
"""

import api_main

def run(beatmap_id: int) -> list:
    # Limit doesn't work
    score_list, status_code = api_main.get_scores(beatmap_id, 3, 50)
    if (status_code != 200):
        return None;    
    
    id_list = [x['user_id'] for x in score_list]
    return id_list
    