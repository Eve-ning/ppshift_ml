# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 07:33:38 2019

@author: user
"""

import save_to
import os
import pandas

csv_location = "D:\\Data Documents\\ppshift\\ppshift_ml\\docs\\regr\\data.csv"
master_data = pandas.read_csv(csv_location, sep=";", header=0, quotechar='@', doublequote=True)

file_names = list(map(int, [x.split('.')[0] for x in os.listdir(save_to.dirs.dir_acd)]))

master_data = master_data[master_data['beatmap_id'].isin(file_names)]
master_data.drop(master_data.columns[6:], axis=1, inplace=True)
master_data = master_data.sort_values(by=['iso_star_rating'])

# =============================================================================
# pandas.set_option('display.max_rows', 500)
# pandas.set_option('display.max_columns', 500)
# pandas.set_option('display.width', 1000)
# =============================================================================

master_data['metadata'] = master_data['artist'] + ' - ' + master_data['title'] + '(' + master_data['version'] + ')'
    
def metadata_from_id(beatmap_id: int):
    
    return (master_data[master_data['beatmap_id'] == beatmap_id].get('metadata').values[0])
    

    
    
    
    
