# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 20:02:04 2019

@author: user
"""

import save_to

OVERRIDE_THRESHOLD = True

# Returns a boolean on if it's within threshold
def within_manipulation_threshold(bpm_list: list, sv_list: list):

    # The 2 rules of keeping within threshold
    # 1: no BPM changes
    # 2: no SV changes
    
    # Check on BPM
    
    # If there's a difference in BPM, this means it's not within threshold
    if (len(bpm_list) > 0):
        
        # We set a buffer as the first value
        bpm_buffer = bpm_list[0]
        
        for bpm in bpm_list:
            if (bpm != bpm_buffer):
                return False
        
    # Same reasoning 
    if (len(sv_list) > 0):
        
        #We set a buffer as the first value
        sv_buffer = sv_list[0]
        
        for sv in sv_list:
            if (sv != sv_buffer):
                return False
            
    return True;

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

def read_osutp(beatmap_id: int):
    osutp_file = open(save_to.dirs.dir_osutp + str(beatmap_id) + ".osutp")
    
    osutp_lines = osutp_file.read().splitlines()

    osutp_lines = [x.split(",") for x in osutp_lines]
    
    osutp_file.close()
    return osutp_lines
    
def read_osuho(beatmap_id: int) :
    osuho_file = open(save_to.dirs.dir_osuho + str(beatmap_id) + ".osuho")
    
    osuho_lines = osuho_file.read().splitlines()

    osuho_lines = [x.split(",") for x in osuho_lines]
    
    osuho_file.close()
    return osuho_lines

def parse_osus_diff(beatmap_id: int):
    if (save_to.exists(save_to.dirs.dir_acd, str(beatmap_id))):
        return []
    
    tp_list = read_osutp(beatmap_id)
    ho_list = read_osuho(beatmap_id)
    
    bpm_list = [bpm[1] for bpm in list(filter(lambda x: x[2] == 'True', tp_list))]
    sv_list = [sv[1] for sv in list(filter(lambda x: x[2] == 'False', tp_list))]
    
    if (OVERRIDE_THRESHOLD):
        return osuho_to_acd(ho_list)
    else:
        thr_pass = within_manipulation_threshold(bpm_list, sv_list)
        print("Treshold Pass: " + str(thr_pass))
        
        if (thr_pass):
            return osuho_to_acd(ho_list)
        
    return []
    
    
def run():

    beatmap_ids = save_to.get_beatmap_ids(save_to.dirs.dir_osuho, save_to.dirs.dir_acd)
    id_len = len(beatmap_ids)
    id_counter = 0
    
    for beatmap_id in beatmap_ids:
        id_counter += 1
        
        print("get: " + str(beatmap_id) + "\t|\t" + str(id_counter) + " out of " + str(id_len))
        
        acd_list = parse_osus_diff(beatmap_id)
        
        if (len(acd_list) == 0):
            continue;
        
        save_to.diff_directory(save_to.dirs.dir_acd, \
                               save_to.flatten_2d_list(acd_list), \
                               str(beatmap_id), "acd")

run()