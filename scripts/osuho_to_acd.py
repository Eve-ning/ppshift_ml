# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 20:02:04 2019

@author: user
"""

column_to_action = {
    4: [2,3,5,6],
    5: [2,3,4,5,6],
    6: [1,2,3,5,6,7],
    7: [1,2,3,4,5,6,7],
    8: [0,1,2,3,5,6,7,8],
    9: [0,1,2,3,4,5,6,7,8],
}

def run(osuho: list, keys: int):
    
    osuho_ = []
    for offset in osuho:
        osuho_.append([offset[0], \
                       offset[1], \
                       column_to_action[keys][offset[2] - 1]])
    osuho = osuho_

    acd = []
    # We will merge the offset and column if it's not an LN
    acd_nn = [[y[0], y[2]] for y in list(filter(lambda x : x[1] == 0, osuho))]
    
    # We will merge the offset and column if it's an LN
    acd_lnh = [[y[0], y[2]] for y in list(filter(lambda x : x[1] != 0, osuho))]
    
    # We will merge the offset_end and column if it's an LN
    acd_lnt = [[-y[1], y[2]] for y in list(filter(lambda x : x[1] != 0, osuho))]

    acd.extend(acd_nn)
    acd.extend(acd_lnh)
    acd.extend(acd_lnt)
    
    return acd;

