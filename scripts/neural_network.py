# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 15:17:26 2019

@author: user
"""

import os
import pandas
import save_to
import keras
import get_beatmap_metadata
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from keras.models import load_model as ld_mdl
import matplotlib.pyplot as plt
import random
import re
import statistics
from datetime import datetime

# MERGES ALL EXISTING DFS
def merge_df(partition: float):
    
    # Get all diff id from the dir
    files = save_to.get_beatmap_ids(save_to.dirs.dir_ppshift)

    # We will filter out < 5 star rating
    files_filter = get_beatmap_metadata.get_id_by_filters(5.0)  
    files = list(filter(lambda x : x in files_filter, files))       
    files = random.sample(files, int(len(files) * partition))
    print("Merging " + str(len(files)) + " files")
    print(files)

    df_list = []
    
    for f in files:
        df = pandas.read_pickle(save_to.dirs.dir_ppshift + str(f) + '.pkl')
        df_list.append(df)
        
    df_all = pandas.concat(df_list)
    df_all.to_pickle(save_to.dirs.dir_ppshift + "\\merge\\merged.pkl")
    
def load_merge():
    
    return pandas.read_pickle(save_to.dirs.dir_ppshift + "\\merge\\merged.pkl")

def model_c():
    
    model = keras.models.Sequential()
    
    model.add(keras.layers.Dense(104, input_shape=(12,), kernel_initializer='normal', activation='relu'))
    model.add(keras.layers.Dense(52))
    model.add(keras.layers.Dense(26))
    model.add(keras.layers.Dense(1, kernel_initializer='normal'))

    model.compile(loss='mean_squared_error', optimizer='adam')
    
    return model

def train_model(model_name: str, frac: float, epochs: int) -> KerasRegressor:
    df = load_merge()   
    
    df_s = df.sample(frac=frac)
    ds_s = df_s.values
    
    in_ds_s = ds_s[:,1:13]
    out_ds_s = ds_s[:,13]
    
    model = model_c()    
    model.fit(in_ds_s, out_ds_s, epochs=epochs, batch_size=1)
    model.model.save(model_name + '.hdf5')
    
    return model

def load_model(model_name: str) -> KerasRegressor:
    
    def dummy():
        return
    model = KerasRegressor(build_fn=dummy, epochs=1, batch_size=10, verbose=1)
    model.model = ld_mdl(model_name + '.hdf5')
    
    return model

def test_model(model: KerasRegressor, beatmap_id: list, model_name: str):
    
    rating_list = []
    log = []
    
    plot_path = 'models\\plots\\' + model_name + '\\'
    
    # Check if plot path is valid
    try:
        # Create target Directory
        os.mkdir(plot_path)
        print(plot_path + " newly created")
    except FileExistsError:
        print(plot_path + " already created")
        
    
    for b_id in beatmap_id:
        df = pandas.read_pickle(save_to.dirs.dir_ppshift + str(b_id) + '.pkl')
        ds = df.values
        
        in_ds = ds[:,1:13]
        out_ds = ds[:,[0,13]]
        
        b_id = int(b_id)
        out_p = model.predict(in_ds, verbose=0)
        
        out_o = pandas.DataFrame(out_ds, columns=['offset','original'])
        out_p = pandas.DataFrame(out_p, columns=['pred'])
        
        out = out_o.join(out_p)
        
        # CREATE PLOTS
        title = get_beatmap_metadata.metadata_from_id([b_id])['metadata'].values[0]
        title = re.sub('[^\w_.)( -]', '', title)
        out.plot(x='offset', title=title)
        
        # Save plot
        plt.savefig(plot_path + title + '.jpg')
        # Do not display plot in IPython console
        plt.close()
        
        # RATE PLOTS
        out['delta'] = out['pred'].subtract(out['original']).abs()
        log.append(str(out['delta'].mean()) + "\t" + \
                   get_beatmap_metadata.metadata_from_id([b_id])['metadata'].values[0])

        rating_list.append(out['delta'].mean())
        
    log.append("mean: " + str(statistics.mean(rating_list)))
    log.append("stdev: " + str(statistics.stdev(rating_list)))
    
    log_f = open(plot_path + "results.txt", "w+")
    log_f.write('\n'.join(log))
    
def random_test_model(maps_to_test: int, model_name: str):
        
    files = list(map(int, [x.split('.')[0] for x in os.listdir(save_to.dirs.dir_ppshift)[0:-1]]))
    # We will filter out < 5 star rating
    files_filter = get_beatmap_metadata.get_id_by_filters(5.0)  
    files = list(filter(lambda x : x in files_filter, files))     
    random_list = random.sample(files, maps_to_test)
    
    test_model(load_model(model_name), random_list, model_name)

model_name = "three_layer"

#merge_df(0.8)
train_model(model_name,0.5,10)
random_test_model(41, model_name)
#test_model( load_model("two_layer"), [1505212], "two_layer_plots")
