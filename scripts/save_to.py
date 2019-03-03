# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 14:38:57 2019

@author: user
"""

import os

class dirs:
    dir_base = "D:\\Data Documents\\ppshift\\ppshift_ml\\docs\\"
    dir_diff = dir_base + "difficulties\\"
    dir_conv = dir_diff + "conversions\\"
    dir_acd = dir_conv + "acd\\"
    dir_osuho = dir_conv + "osuho\\"
    dir_osutp = dir_conv + "osutp\\"


def diff_directory(path: dirs, data_list: list, filename: str, extension: str):
    beatmap_file = open(path + filename + "." + extension, "w+", encoding="utf-8")
    
    for data in data_list:
        dataj = ",".join(tuple(map(str, data)))
        beatmap_file.write(dataj + "\n")
      
    beatmap_file.close()
    
    
def exists(path: dirs, filename: str):
    # We get all file names (excluding folders) <excluded by lambda filter>
    dir_files = [x.split(".")[0] for x in list(filter(lambda n: n.count('.') != 0, os.listdir(path)))]

    return filename in dir_files



print(exists(dirs.dir_acd,str(429552)))
print(exists(dirs.dir_acd,str(429553)))