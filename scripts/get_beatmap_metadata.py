# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 07:33:38 2019

@author: user
"""

#import save_to
#import os
import pandas

csv_location = "D:\\Data Documents\\ppshift\\ppshift_ml\\documents\\beatmap_info\\data.csv"

def get_csv():
        
    master_data = pandas.read_csv(csv_location, sep=";", quotechar='@', doublequote=True)
    return master_data

def metadata_from_id(beatmap_id: list):
    
    master_data = get_csv()
    master_data.drop(master_data.columns[6:], axis=1, inplace=True)
    
    master_data['metadata'] = master_data['artist'] + ' - ' + master_data['title'] + '(' + master_data['version'] + ')'
       
    return (master_data[master_data['beatmap_id'].isin(beatmap_id)])
    
def get_id_by_filters(min_star_rating:float = 3.5):
    master_data = get_csv()
    
    master_data = master_data[master_data['iso_star_rating'] > min_star_rating]
    return master_data['beatmap_id'].values

