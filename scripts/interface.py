# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 18:06:45 2019

@author: user
"""

import interface_class
import api_main
import interface_neural_network
import os

beatmap_info_path = \
"D:\\Data Documents\\ppshift\\ppshift_ml\\documents\\beatmap_info\\beatmap_info.txt"

# This is where we use interface_class

def download_beatmap_info(YYYYMMDD: str, until_YYYYMMDD: str):
    
    data = api_main.get_beatmaps_since_ext(YYYYMMDD, until_YYYYMMDD)
    f = open(beatmap_info_path, "w+", encoding="utf-8")
    f.write(str(data))
        
    return

def load_beatmap_info():
    
    f = open(beatmap_info_path, "r", encoding="utf-8")
    return eval(f.read())

def get_ids(star_rating_below:float = 100,
            star_rating_above:float = 0,
            ranked_before_YYYYMMDD:str = '20190101',
            ranked_after_YYYYMMDD:str = '20170101'):
    
    bm_info_l = load_beatmap_info()
    output_l = []
    for bm_info in bm_info_l:
        
        YYYYMMDD = bm_info['approved_date']
        # Shift forward latest
        YYYYMMDD = int(YYYYMMDD[0:4] + \
                       YYYYMMDD[5:7] + \
                       YYYYMMDD[8:10])
        
        if (float(bm_info['difficultyrating']) >= star_rating_above and \
            float(bm_info['difficultyrating']) <= star_rating_below and \
            YYYYMMDD <= ranked_before_YYYYMMDD and \
            YYYYMMDD >= ranked_after_YYYYMMDD):
            output_l.append(int(bm_info['beatmap_id']))
    
    return output_l

def parse_ids():
    # bm_ids = get_ids(star_rating_above=5)
    
    # Parsing a custom made id list
    f = open("D:\\Data Documents\\ppshift\\ppshift_ml\\documents\\beatmap_info\\beatmap_ids.csv",'r')
    bm_ids = f.read().splitlines()
    bm_ids = list(map(int, bm_ids))
    counter = 1
    
    for bm_id in bm_ids:
        try:
            print('[' + str(counter) + ']', end='\t')
            bm = interface_class.parse_beatmap_id(beatmap_id=bm_id, soft_load_flag=True)
            bm.parse_osu()
        except:
            
            print (str(bm_id) + ' ERROR')
            pass
        
        counter += 1
        
def parse_evals():
    file_list = [x.split('.')[0] for x in os.listdir("D:\\Data Documents\\ppshift\\ppshift_ml\\documents\\eval\\osu\\")]
    
    for file in file_list:
        bm = interface_class.parse_beatmap_file_name(beatmap_file_name=file, soft_load_flag=True)
        bm.parse_osu()
        
def train_model(model_name: str, seed: int = None):
    nn = interface_neural_network.train_model(model_name, seed)
    
    # Model 9
    nn.layer_1_nrns = 96
    nn.layer_2_nrns = 48 
    nn.layer_3_nrns = 24 
    
    nn.train(50, 50)
    
def test_model(model_name: str, seed: int = None):
    nn = interface_neural_network.train_model(model_name, seed)
    nn.test()
    
def eval_model(model_name: str):
    nn = interface_neural_network.eval_model(model_name)
    nn.evaluate()
    return

# download_beatmap_info("20130101","20190313")

parse_evals()
eval_model("e50_50_96_48r2_1_24r2_1_s10")
    
# model_name = "e50_50_96_48r2_1_24r2_1_s10"
# seed = 10

# train_model(model_name, seed)
# test_model(model_name, seed)