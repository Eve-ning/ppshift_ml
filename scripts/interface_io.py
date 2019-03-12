# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 13:13:08 2019

@author: user
"""
import os

class interface_io:
    
    def __init__(self, beatmap_id: int):
        self.beatmap_id = beatmap_id
        self.base_dir = "D:\\Data Documents\\ppshift\\ppshift_ml\\docs\\difficulties\\conversions\\"
        
    def load_nested(self, file_type: str, nest: str, suffix: str):
        
        path_dir = self.base_dir + file_type + '\\' + nest + '\\'
        path = path_dir + str(self.beatmap_id) + '_' + suffix + '.' + file_type
        
        try:
            f = open(path, 'r')
            out = eval(f.read())
            f.close()
            return out
        except:
            print("Failed to read: {path}".format(path=path))
            return None
        
    def load(self, file_type: str) -> list:

        path_dir = self.base_dir + file_type + '\\'
        path = path_dir + str(self.beatmap_id) + '.' + file_type

        try:
            f = open(path, 'r')
            out = eval(f.read())
            f.close()
            return out
        except:
            print("Failed to read: {path}".format(path=path))
            return None
        
    def save_nested(self, file_type:str, nest: str, suffix: str, data: str, \
                    skip_if_exist: bool):
        
        path_dir = self.base_dir + file_type + '\\' + nest + '\\'
        path = path_dir + str(self.beatmap_id) + '_' + suffix + '.' + file_type
        
        try:
            os.mkdir(path_dir)
            print("Creating directory: {dir}".format(dir = path_dir))
        except:
            pass
        
        if (skip_if_exist and os.path.isfile(path)):
            print("Skipping: {path}".format(path=path))
        
        try:
            f = open(path, 'w+')
            f.write(data)
            f.close()
            return True
        except:
            print("Failed to save: {path}".format(path=path))
            return False

    def save(self, file_type: str, data: str, skip_if_exist: bool):

        path_dir = self.base_dir + file_type + '\\'
        path = path_dir + str(self.beatmap_id) + '.' + file_type
        
        try:
            os.mkdir(path_dir)
            print("Creating directory: {dir}".format(dir = path_dir))
        except:
            pass
        
        if (skip_if_exist and os.path.isfile(path)):
            print("Skipping: {path}".format(path=path))
        
        try:
            f = open(path, 'w+')
            f.write(data)
            f.close()
            return True
        except:
            print("Failed to save: {path}".format(path=path))
            return False

        
        
    
    
    
    
    
    
    
    
    
    