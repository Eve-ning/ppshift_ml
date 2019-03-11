# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 20:02:04 2019

@author: user
"""


def osuho_to_acd(osuho: list):
    
    # Fix acd starting from 0 by adding 1
    acd_nn = [[ho[0], str(int(ho[2]) + 1)] for ho in list(filter(lambda ho: ho[1] == "0", osuho))]
    acd_lnh = [[ho[0],"+" + str(int(ho[2]) + 1)] for ho in list(filter(lambda ho: ho[1] != "0", osuho))]
    acd_lnt = [[ho[1],"-" + str(int(ho[2]) + 1)] for ho in list(filter(lambda ho: ho[1] != "0", osuho))]
    
    acd = []
    acd.extend(acd_nn)
    acd.extend(acd_lnh)
    acd.extend(acd_lnt)
    
    return acd;

def run(beatmap_id: int):
    if (save_to.exists(save_to.dirs.dir_acd, str(beatmap_id))):
        return []
    
    tp_list = read_osutp(beatmap_id)
    ho_list = read_osuho(beatmap_id)
    
    bpm_list = [bpm[1] for bpm in list(filter(lambda x: x[2] == 'True', tp_list))]
    sv_list = [sv[1] for sv in list(filter(lambda x: x[2] == 'False', tp_list))]
    

    return osuho_to_acd(ho_list)

    

run()