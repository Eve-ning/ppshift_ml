# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 15:17:26 2019

@author: user
"""

import os
import pandas
import save_to
import numpy
import keras
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn import preprocessing

# MERGES ALL EXISTING DFS
def merge_df():
    
    # Get all diff id from the dir
    files = os.listdir(save_to.dirs.dir_ppshift)            

    df_list = []
    
    for f in files:
        df = pandas.read_pickle(save_to.dirs.dir_ppshift + f)
        df_list.append(df)
        
    df_all = pandas.concat(df_list)
    df_all.to_pickle(save_to.dirs.dir_ppshift + "merged.pkl")
    
def load_merge():
    
    return pandas.read_pickle(save_to.dirs.dir_ppshift + "1231418.pkl")

# =============================================================================
# # 15 labels
# print(pandas.read_pickle(save_to.dirs.dir_ppshift + "merged.pkl").columns)
# =============================================================================

def model_c():
    model = keras.models.Sequential()
    model.add(keras.layers.Dense(14, input_shape=(14,), kernel_initializer='normal', activation='sigmoid'))
    model.add(keras.layers.Dense(7))
    model.add(keras.layers.Dense(1))
    
    sgd = keras.optimizers.SGD(lr=0.01, momentum=0.7)
    
    model.compile(loss=keras.losses.mean_squared_error, optimizer=sgd,metrics=['accuracy'])
    
    return model

seed = 1

df = load_merge()   
df_s = df.sample(frac=0.5, random_state=seed)
df_t = df.sample(frac=0.2, random_state=seed+1)

ds_s = df_s.values
ds_t = df_t.values
#
#ds_s = preprocessing.MinMaxScaler().fit_transform(ds_s)
#ds_t = preprocessing.MinMaxScaler().fit_transform(ds_t) 

in_ds_s = ds_s[:,0:14]
out_ds_s = ds_s[:,14]

print(in_ds_s)

in_ds_t = ds_t[:,0:14]
out_ds_t = ds_t[:,14]

#estimator = keras.wrappers.scikit_learn.KerasRegressor(build_fn=model_c, epochs=10, batch_size=10, verbose=1)
model = model_c()
model.fit(in_ds_s,out_ds_s, epochs=5, batch_size=5, verbose=1)

scores =model.evaluate(in_ds_t,out_ds_t, verbose=1)

print(scores)

df_v = pandas.read_pickle(save_to.dirs.dir_ppshift + "1104774.pkl")

ds_v = df_v.values
ds_v = ds_v[:,0:14]
predictions = model.predict(ds_v)
print(predictions)

# =============================================================================
# 	
# kfold = KFold(n_splits=10, random_state=seed)
# results = cross_val_score(estimator, in_ds_s, out_ds_s, cv=kfold)
# print("Results: %.2f (%.2f) MSE" % (results.mean(), results.std()))
# =============================================================================
