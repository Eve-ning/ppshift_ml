# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 20:57:03 2019

@author: user
"""

import interface
import os

info = interface.load_beatmap_info()

id_matches = []

local_ids = [x.split('.')[0] for x in os.listdir("D:\\Data Documents\\ppshift\\ppshift_ml\\documents\\acr")]
local_ids = list(map(int, local_ids))

# Loop through all beatmaps and find out which have bias
for bm in info:
    if (bm['diff_size'] == '8' and int(bm['beatmap_id']) in local_ids):
        id_matches.append(int(bm['beatmap_id']))

spec_style_l = []

for id_match in id_matches:
    f = open('D:\\Data Documents\\ppshift\\ppshift_ml\\documents\\osu\\' + str(id_match) + '.osu', 'r', encoding='utf-8')
    
    print(id_match)
    filestr_l = f.read().splitlines()
    f.close()
    locater_str = ''
    locater_counter = 0
    while (not locater_str.startswith('SpecialStyle:')):
        locater_str = filestr_l[locater_counter]
        locater_counter += 1
    
    spec_style_l.append([id_match, int(locater_str.split(':')[1]) == 1])

print(spec_style_l)
    

