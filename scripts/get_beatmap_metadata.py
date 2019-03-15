# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 07:33:38 2019

@author: user
"""

info_location = "D:\\Data Documents\\ppshift\\ppshift_ml\\documents\\beatmap_info\\beatmap_info.txt"

def get_info():
        
    f = open(info_location, 'r', encoding='utf-8')
    output = eval(f.read())
    f.close()
    return output

def metadata_from_id(beatmap_id: int):
    
    master_data = get_info()
    
    for bm in master_data:
        if (int(bm['beatmap_id']) == beatmap_id):
            metadata = bm['artist'] + ' - ' + \
                       bm['title'] + ' (' + \
                       bm['version'] + ') <' + \
                       bm['creator'] + '>'
            return metadata
