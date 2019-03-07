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
    

def diff_directory(path: dirs, data_list: list, filename: str, extension: str, join: bool = True):
    beatmap_file = open(path + filename + "." + extension, "w+", encoding="utf-8")
    
    for data in data_list:
        if (join == True):
            dataj = ",".join(tuple(map(str, data)))
        else:  
            dataj = data
        beatmap_file.write(dataj + "\n")
      
    beatmap_file.close()
    
    
def exists(path: dirs, filename: str):
    # We get all file names (excluding folders) <excluded by lambda filter>
    dir_files = [x.split(".")[0] for x in list(filter(lambda n: n.count('.') != 0, os.listdir(path)))]
    
    exists_flag = filename in dir_files
    if (exists_flag):
        print("Skipping: " + filename)

    return exists_flag

# =============================================================================
# def custom_func():
#     ids = [x.split('.')[0] for x in os.listdir(dirs.dir_plyrid)]
#     acds = [x.split('.')[0] for x in os.listdir(dirs.dir_acd)]
#     
#     for id_ in ids:
#         if (id_ not in acds):
#             idf = open(dirs.dir_plyrid + id_ + ".plyrid", "w+")
#             idf.write("999" * 99)
#             
#             
# custom_func()
# =============================================================================
