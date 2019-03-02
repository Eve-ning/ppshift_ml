# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 18:13:05 2019

@author: user
"""
import os

diff_dir = "D:\\Data Documents\\ppshift\\ppshift_ml\\docs\\difficulties\\"

# returns offset, value, is_bpm
def read_timing_point(tp: str):
    tp_list = tp.split(",")
    offset = int(round(float(tp_list[0])))
    value = (60000.0 if tp_list[6] == '1' else -100.0) / float(tp_list[1])
    
    return offset, value, tp_list[6] == '1'
    
# returns offset, offset_end(0 if normal note), column
def read_hit_object(ho: str, keys: int):       
    ho_list = ho.split(",")
    offset = int(ho_list[2])
    offset_end = int(ho_list[5].split(":")[0]) if ho.count(":") == 5 else 0
    column = round((int(ho_list[0]) * keys - 256)/512)
    
    return offset, offset_end, column

# Saves difficulty as .osus (osu simple)
def save_osu_diff(ho_list: list, tp_list: list, beatmap_id: int):
    beatmap_file = open(diff_dir + "conversions\\osus\\" + str(beatmap_id) + ".osus", "w+", encoding="utf-8")
    
    for tp in tp_list:
        tpj = ",".join(tuple(map(str,tp)))
        beatmap_file.write("TP," + tpj + "\n")
        
    for ho in ho_list:
        hoj = ",".join(tuple(map(str,ho)))
        beatmap_file.write("HO," + hoj + "\n")
        
    beatmap_file.close()
    
# Checks if the convert already exists
def check_osus_exist(beatmap_id: int):
    
    files = os.listdir(diff_dir + "conversions\\osus")
    beatmap_id_w_ext = str(beatmap_id) + '.osus'
    return beatmap_id_w_ext in files
    
# We take a beatmap_id as an input
# We will create a separate file format for easier reading
def parse_osu_diff(beatmap_id: int):
    
    if (check_osus_exist(beatmap_id)):
        print("skipping: " + str(beatmap_id))
        return (),();
        
    beatmap_file = open(diff_dir + str(beatmap_id) + ".osu", 'r', encoding="utf-8")
    beatmap_lines = beatmap_file.readlines()
    
    counter = 0

    tp_list = []
    ho_list = []
    circleSize = 0
    
    # Find CircleSize:

    # Find [TimingPoints]
    while (not "TimingPoint" in beatmap_lines[counter]) and counter < len(beatmap_lines):
        if (beatmap_lines[counter].startswith("CircleSize:")):
            circleSize = int(beatmap_lines[counter].split(":")[1]) # Circle Size will always be 1 digit
            print (circleSize)
        counter += 1

    # Skip Tag
    counter += 1
    
    # Find [HitObject]
    while (not "HitObject" in beatmap_lines[counter]) and counter < len(beatmap_lines):
        
        # Append for all Timing Point
        if (beatmap_lines[counter][0].isdigit()):
            tp_list.append(read_timing_point(beatmap_lines[counter]))
        
        counter += 1
            
    # Skip Tag
    counter += 1
    
    while counter < len(beatmap_lines):
        
        # Append for all Hit Object
        if (beatmap_lines[counter][0].isdigit()):
            ho_list.append(read_hit_object(beatmap_lines[counter], circleSize))
            
        counter += 1
            
#    print("hitobjects")
#    print(ho_list)
#    
#    print("timingpoints")
#    print(tp_list)
    
    beatmap_file.close()
    
    return ho_list, tp_list
    
def main():

    files = os.listdir(diff_dir)
    files_len = len(files)
    files_counter = 0
    
    for f in files:
        files_counter += 1
        
        # Skip non .osu files
        if (not ".osu" in f):
            continue
        
        beatmap_id = str(f.split(".")[0])
        print("get: " + str(beatmap_id) + "\t|\t" + str(files_counter) + " out of " + str(files_len))
        
        ho_list, tp_list = parse_osu_diff(beatmap_id)
        if (len(ho_list) == 0):
            continue;
        
        save_osu_diff(ho_list, tp_list, beatmap_id), 
        
        
if __name__== "__main__":
    main()
