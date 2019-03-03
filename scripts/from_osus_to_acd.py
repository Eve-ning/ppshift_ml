# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 20:02:04 2019

@author: user
"""

import os
import save_to

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
    acd_nn = [[ho[0], ho[2]] for ho in list(filter(lambda ho: ho[1] == "0", osuho))]
    acd_lnh = [[ho[0],"+" + ho[2]] for ho in list(filter(lambda ho: ho[1] != "0", osuho))]
    acd_lnt = [[ho[1],"-" + ho[2]] for ho in list(filter(lambda ho: ho[1] != "0", osuho))]
    
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
        print("skipping: " + str(beatmap_id))
        return []
    
    tp_list = read_osutp(beatmap_id)
    ho_list = read_osuho(beatmap_id)
    
    bpm_list = [bpm[1] for bpm in list(filter(lambda x: x[2] == 'True', tp_list))]
    sv_list = [sv[1] for sv in list(filter(lambda x: x[2] == 'False', tp_list))]
    
    thr_pass = within_manipulation_threshold(bpm_list, sv_list)
    print("Treshold Pass: " + str(thr_pass))
    
    if (thr_pass):
        return osuho_to_acd(ho_list)
    
    return []
    
#parse_osus_diff(888279)
    
def main():

    # Get all diff id from the dir
    files = os.listdir(save_to.dirs.dir_osuho)
    files_len = len(files)
    files_counter = 0
    
    for f in files:
        files_counter += 1
        
        # Skip non .osuho files
        if (not ".osuho" in f):
            continue
        
        # Extract Ids
        beatmap_id = str(f.split(".")[0])
        print("get: " + str(beatmap_id) + "\t|\t" + str(files_counter) + " out of " + str(files_len))
        
        acd_list = parse_osus_diff(beatmap_id)
        if (len(acd_list) == 0):
            continue;
        
        save_to.diff_directory(save_to.dirs.dir_acd, acd_list, str(beatmap_id), "acd")
        
        
if __name__== "__main__":
    main()
    
    
    
    
    