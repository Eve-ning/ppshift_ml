# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 11:24:37 2019

@author: user
"""
import os

import osuho_to_acd

acr_dir = "D:\\Data Documents\\ppshift\\ppshift_ml\\documents\\acr\\"

file_paths = list(filter(lambda x : x.count('.') > 0, os.listdir(acr_dir)))
file_count = len(file_paths)  - 182

counter = 0 


for file_path in file_paths[182:]:
    
    print(str(counter) + " / " + str(file_count))
    file_str_output = []
    
    file_r = open(acr_dir + file_path, "r")
    file_str_lines = file_r.read().splitlines()
    file_r.close()
    
    # Get key
    file_str_temp = eval(file_str_lines[25])
    file_str_temp = [x[1] for x in file_str_temp]
    keys = max(file_str_temp)

    for file_str_line in file_str_lines:
        #Skip dummy
        if (len(file_str_line) < 10):
            continue
        
        file_str_line = eval(file_str_line)
        file_str_output_part = []
        
        weird_key_flag = False
        
        for pair in file_str_line:

            if (not weird_key_flag and pair[1] == -9):
                weird_key_flag = True
                continue
            is_neg = pair[1] < 0
            
            file_str_output_part.append([pair[0], \
                                         (-1 if is_neg else 1) * 
                                         osuho_to_acd.column_to_action[keys][abs(pair[1]) - 1]])
        file_str_output.append(str(file_str_output_part).replace('[[','[').replace(']]',']'))

    file_w = open(acr_dir + "conv\\" + file_path, "w+")
    
    file_w.write('\n'.join(file_str_output))
    file_w.close()
    
    counter += 1
    
