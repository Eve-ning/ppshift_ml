# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 20:02:04 2019

@author: user
"""

import pandas

column_to_action = {
    4: [2,3,5,6],
    5: [2,3,4,5,6],
    6: [1,2,3,5,6,7],
    7: [1,2,3,4,5,6,7],
    8: [0,1,2,3,5,6,7,8],
    9: [0,1,2,3,4,5,6,7,8],
}

def run(osuho: pandas.DataFrame, keys: int) -> pandas.DataFrame:
    
    osuho['column'] = convert_column_to_action(osuho['column'], keys)
    
    # We will merge the offset and column if it's not an LN
    acd_nn = pandas.concat([osuho['offset'][osuho['offset_end'] == 0],\
                            osuho['column'][osuho['offset_end'] == 0]], axis=1)
    
    # We will merge the offset and column if it's an LN
    acd_lnh = pandas.concat([osuho['offset'][osuho['offset_end'] != 0],\
                             osuho['column'][osuho['offset_end'] != 0]], axis=1)
    
    # We will merge the offset_end and column if it's an LN
    acd_lnt = pandas.concat([osuho['offset_end'][osuho['offset_end'] != 0],\
                             osuho['column'][osuho['offset_end'] != 0]], axis=1)
    
    acd_lnt['column'] = [-x for x in acd_lnt['column']]
    acd_lnt.rename(index=str, columns={"offset_end": "offset"})
    
    acd = pandas.concat([acd_nn, acd_lnh, acd_lnt], axis=0)
    
    acd.rename(index=str, columns={"column": "action"})
    
    return acd;

def convert_column_to_action(column: pandas.Series, keys: int):
    # Columns start from 1, so we need to minus off 1
    return [column_to_action[keys][x - 1] for x in column]