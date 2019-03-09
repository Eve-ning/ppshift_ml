# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 14:38:57 2019

@author: user
"""

import os

class dirs:
    dir_doc = "D:\\Data Documents\\ppshift\\ppshift_ml\\docs\\"
    dir_diff = dir_doc + "difficulties\\"
    dir_conv = dir_diff + "conversions\\"
    dir_acd = dir_conv + "acd\\"
    dir_osuho = dir_conv + "osuho\\"
    dir_osutp = dir_conv + "osutp\\"
    dir_plyrid = dir_conv + "plyrid\\"
    dir_acr = dir_conv + "acr\\"
    dir_acrv = dir_conv + "acrv\\"
    dir_ppshift = dir_conv + "ppshift\\"
    

def diff_directory(path: dirs, str_data_list: list, filename: str, extension: str, join: bool = True):
    beatmap_file = open(path + filename + "." + extension, "w+", encoding="utf-8")
    
    for data in str_data_list:

        beatmap_file.write(data + "\n")
      
    beatmap_file.close()
    
def flatten_2d_list(data: list):
    # Squish all data in a 2d list for saving
    
    str_data = []
    for x in data:
        # convert all into str
        x = list(map(str, x))
        str_data.append(','.join(x))
        
    return str_data
    
def exists(path: dirs, filename: str):
    # We get all file names (excluding folders) <excluded by lambda filter>
    dir_files = [x.split(".")[0] for x in list(filter(lambda n: n.count('.') != 0, os.listdir(path)))]
    
    exists_flag = filename in dir_files
    if (exists_flag):
        print("Skipping: " + filename)

    return exists_flag

def get_beatmap_ids(path: dirs, compare_exist: dirs = None) -> list:
    files = list(filter(lambda x: x.count('.') == 1, os.listdir(path)))
    files = [x.split('.')[0] for x in files]
    
    files = list(map(int, files))
    
    if (compare_exist == None):
        return files
    
    compare_files = list(filter(lambda x: x.count('.') == 1, os.listdir(compare_exist)))
    compare_files = [x.split('.')[0] for x in compare_files]
    
    compare_files = list(map(int, compare_files))

    # Get all files not in the compare dir
    files = list(filter(lambda x : x not in compare_files, files))
    
    return files


