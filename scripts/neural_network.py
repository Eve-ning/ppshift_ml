# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 15:17:26 2019

@author: user
"""

import os
import pandas
import save_to
import keras

	
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# MERGES ALL EXISTING DFS
def merge_df():
    
    # Get all diff id from the dir
    files = os.listdir(save_to.dirs.dir_ppshift)            
    counter = 0
    
#    glob_df = pandas.read_pickle(save_to.dirs.dir_ppshift + files[0])
    df_list = []
    
    for f in files:
        counter += 1
        df = pandas.read_pickle(save_to.dirs.dir_ppshift + f)
        df_list.append(df)
        
    df_all = pandas.concat(df_list)
    df_all.to_pickle(save_to.dirs.dir_ppshift + "merged.pkl")
    
def load_merge():
    
    return pandas.read_pickle(save_to.dirs.dir_ppshift + "merged.pkl")

