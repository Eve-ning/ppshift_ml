# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 13:13:08 2019

@author: user
"""
import os

class interface_io:
    
    def __init__(self, beatmap_file_name: str, base_dir:str = "D:\\Data Documents\\ppshift\\ppshift_ml\\documents\\"):
        self.beatmap_file_name = beatmap_file_name
        self.base_dir = base_dir
        
    def exist(self, file_type: str) -> bool:
        path_dir = self.base_dir + file_type + '\\'
        path = path_dir + str(self.beatmap_file_name) + '.' + file_type
        
        return True if os.path.isfile(path) else None

    def load(self, file_type: str, custom_folder_name: str=None) -> list:

        if (custom_folder_name == None):
            custom_folder_name = file_type
            
        path_dir = self.base_dir + file_type + '\\'
        path = path_dir + str(self.beatmap_file_name) + '.' + file_type

        try:
            f = open(path, 'r', encoding='utf-8')
            out = f.read()
            f.close()
            return out
        except:
            print("Failed to read: {path}".format(path=path))
            return None


    def save(self, file_type: str, data, skip_if_exist: bool, \
             custom_folder_name: str=None) -> bool:

        if (custom_folder_name == None):
            custom_folder_name = file_type
        
        path_dir = self.base_dir + custom_folder_name + '\\'
        path = path_dir + str(self.beatmap_file_name) + '.' + file_type
        
        try:
            os.mkdir(path_dir)
            print("Creating directory: {dir}".format(dir = path_dir))
        except:
            pass
        
        if (skip_if_exist and os.path.isfile(path)):
            print("Skipping: {path}".format(path=path))
            return True
        
        try:
            f = open(path, 'w+')
            f.write(data)
            f.close()
            return True
        except:
            print("Failed to save: {path}".format(path=path))
            return False

        
   

# =============================================================================
#     def load_nested(self, file_type: str, nest: str, suffix: str):
#         
#         path_dir = self.base_dir + file_type + '\\' + nest + '\\'
#         path = path_dir + str(self.beatmap_id) + '_' + suffix + '.' + file_type
#         
#         try:
#             f = open(path, 'r', encoding='utf-8')
#             out = f.read()
#             f.close()
#             return out
#         except:
#             print("Failed to read: {path}".format(path=path))
#             return None
# =============================================================================
        
        
# =============================================================================
#     def save_nested(self, file_type:str, nest: str, suffix: str, data: str, \
#                     skip_if_exist: bool):
#         
#         data = str(data)
#         
#         path_dir = self.base_dir + file_type + '\\' + nest + '\\'
#         path = path_dir + str(self.beatmap_id) + '_' + suffix + '.' + file_type
#         
#         try:
#             os.mkdir(path_dir)
#             print("Creating directory: {dir}".format(dir = path_dir))
#         except:
#             pass
#         
#         if (skip_if_exist and os.path.isfile(path)):
#             print("Skipping: {path}".format(path=path))
#             return True
#         
#         try:
#             f = open(path, 'w+')
#             f.write(data)
#             f.close()
#             return True
#         except:
#             print("Failed to save: {path}".format(path=path))
#             return False
# =============================================================================  
    
    
    
    
    
    
    