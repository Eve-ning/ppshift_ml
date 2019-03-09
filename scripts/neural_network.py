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
from sklearn import preprocessing
from keras.models import load_model as ld_mdl
import matplotlib.pyplot as plt
import random
import re
import statistics
from keras.utils import plot_model

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
    
    model.add(keras.layers.Dense(104, input_shape=(13,), kernel_initializer='normal', activation='relu'))
    model.add(keras.layers.Dense(52))
    model.add(keras.layers.Dropout(0.3))
    model.add(keras.layers.Dense(26))
    model.add(keras.layers.Dense(1, kernel_initializer='normal'))
    
    plot_model(model, to_file="three" + ".png")
    
    model.compile(loss='mean_squared_error', optimizer='adam')
    
    return model

def train_model(model_name: str) -> KerasRegressor:
    seed = 1
    
    df = load_merge()   
    
    df_s = df.sample(frac=0.010, random_state=seed)
    
    ds_s = df_s.values
    
    min_max_scaler = preprocessing.MinMaxScaler()
    ds_s = min_max_scaler.fit_transform(ds_s)

    in_ds_s = ds_s[:,1:14]
    out_ds_s = ds_s[:,14]
    
    model = model_c()
    
    estimator = KerasRegressor(build_fn=model_c, epochs=15, batch_size=1, verbose=1)
    
    kfold = KFold(n_splits=3, random_state=seed)
    results = cross_val_score(estimator, in_ds_s, out_ds_s, cv=kfold)
    print("Results: %.2f (%.2f) MSE" % (results.mean(), results.std()))
    
    model.fit(in_ds_s, out_ds_s)
    model.model.save(model_name + '.hdf5')
    
    return model

def load_model(model_name: str) -> KerasRegressor:
    
    def dummy():
        return
    model = KerasRegressor(build_fn=dummy, epochs=1, batch_size=10, verbose=1)
    model.model = ld_mdl(model_name + '.hdf5')
    
    return model

def test_model(model: KerasRegressor, beatmap_id: list, sub_folder: str = 'plots'):
    
    rating_list = []
    
    for b_id in beatmap_id:
        df = pandas.read_pickle(save_to.dirs.dir_ppshift + str(b_id) + '.pkl')
    #    Partitions the test by 33% - 66%
    #    df = df[(df.index>numpy.percentile(df.index, 33)) & (df.index<=numpy.percentile(df.index, 66))]
        ds = df.values
        
        min_max_scaler = preprocessing.MinMaxScaler()
        ds = min_max_scaler.fit_transform(ds)
        
        in_ds = ds[:,1:14]
        out_ds = ds[:,[0,14]]
        
        b_id = int(b_id)
        out_p = model.predict(in_ds, verbose=0)
        
        out_o = pandas.DataFrame(out_ds, columns=['offset','original'])
        out_p = pandas.DataFrame(out_p, columns=['pred'])
        
        out = out_o.join(out_p)
        
        title = get_beatmap_metadata.metadata_from_id([b_id])['metadata'].values[0]
        title = re.sub('[^\w_.)( -]', '', title)
        out.plot(x='offset', title=title)
        plt.savefig(sub_folder + '\\' + title + '.jpg')
        plt.close()

        print("Rating: " + str(out['pred'].mean() / out['original'].mean()) + "\t", end='')
        print(get_beatmap_metadata.metadata_from_id([b_id])['metadata'].values[0])
        
        rating_list.append(out['pred'].mean() / out['original'].mean())
        
    print("mean: " + str(statistics.mean(rating_list)))
    print("stdev: " + str(statistics.stdev(rating_list)))
    
def random_test_model(maps_to_test: int, model_name: str, sub_folder: str = 'plots'):
        
    files = list(map(int, [x.split('.')[0] for x in os.listdir(save_to.dirs.dir_ppshift)[0:-1]]))
    # We will filter out < 5 star rating
    files_filter = get_beatmap_metadata.get_id_by_filters(5.0)  
    files = list(filter(lambda x : x in files_filter, files))     
    random_list = random.sample(files, maps_to_test)
    
    test_model(load_model(model_name), random_list, sub_folder)


#merge_df(0.8)
train_model("three_layer")
random_test_model(41, "three_layer", "three_layer_plots")
#test_model( load_model("two_layer"), [1505212], "two_layer_plots")
