# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 13:13:08 2019

@author: user
"""

import pickle
import os

base_dir = "D:\\Data Documents\\ppshift\\ppshift_ml\\documents\\"

def load_pkl(beatmap_id: int, file_type: str, file_extension: str = 'pkl'):
    
    path = base_dir + file_type + '\\' + str(beatmap_id) + '.' + file_extension
    
    try:
        with open(path, 'r') as f:
            data = pickle.load(f)    
        return data
    except:
        return None
    
def save_pkl(beatmap_id: int, data, file_type: str, \
             file_extension: str = 'pkl', create_dir: bool = True):

    path = base_dir + file_type + '\\' + str(beatmap_id) + '.' + file_extension
    
    if (create_dir):
        try:  
            os.mkdir(path)
        except OSError:  
            print ("Path %s exists" % path)
        else:  
            print ("Created path %s" % path)
        
    try:
        with open(path, 'w+') as f:
            pickle.dump(data, f)
        return True
    except:
        return False