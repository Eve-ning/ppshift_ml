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
        return [];
    
    username_list, id_list = [[x['username'], x['user_id']] for x in score_list]

    print(username_list)

get_player_ids(823842)

# =============================================================================
# print(api_main.get_replay(823842, 3, 1824775))
# =============================================================================


