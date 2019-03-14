# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 15:17:26 2019

@author: user
"""

import os
import pandas
import keras
import get_beatmap_metadata
from keras.wrappers.scikit_learn import KerasRegressor
from keras.models import load_model as ld_mdl
import matplotlib.pyplot as plt
import random
import re
import statistics

class model:
    
    def __init__(self, training_split: float = 0.8, model_name: str):
        self.ppshift_dir = "D:\\Data Documents\\ppshift\\ppshift_ml\\documents\\ppshift\\"
        
        # We will define training and test split here
        
        
        self.training_split = training_split
        self.test_split = 1 - training_split
        self.model_name = model_name
        
        self.plot_dir = "D:\\Data Documents\\ppshift\\ppshift_ml\\documents\\neural_network\\plots\\" + \
                        model_name + "\\"
                        
        
    
    def train(self, bm_id_list: list, epochs: int, batch_size):
        self._load_training(bm_id_list)
        self._train_model(self.model_name, epochs, batch_size)
    
    def _load_training(self, bm_id_list: list): 
             
        # We get a random sample of the list
        bm_id_list = random.sample(bm_id_list,\
                                   int(len(bm_id_list) * self.training_split))
        
        print("Merging " + str(len(bm_id_list)) + " files")
        print(bm_id_list)
    
        ppshift_list = []
        
        for bm_id in bm_id_list:
            ppshift_f = open(self.ppshift_dir + str(bm_id) + '.ppshift', 'r')
            # Important: The first 29 results has a 0 output, so we will cut
            # those results out with splicing.
            # This is due to the rolling Aggregation
            ppshift_str = ppshift_f.read().splitlines()[29:]
            ppshift_f.close()   
            ppshift_list.extend(list(map(eval, ppshift_str)))
            
        self.training_df = \
        pandas.DataFrame(ppshift_list,\
                         columns=['OFF','LP','LR','LM','LI','S', \
                                  'RI','RM','RR','RP','NN','LNH','LNT','MED'])
    
        return
    
    def _model_c(self):
        
        model = keras.models.Sequential()
        
        model.add(keras.layers.Dense(96, input_shape=(12,), \
                                     kernel_initializer='normal', \
                                     activation='relu'))
        model.add(keras.layers.Dense(48))
        model.add(keras.layers.Dense(24))
        model.add(keras.layers.Dense(1, kernel_initializer='normal'))
    
        model.compile(loss='mean_squared_error', optimizer='adam')
        
        return model
    
    def _train_model(self, model_name: str, epochs: int, batch_size: int):
        
        df = self.training_df 

        # Shuffle
        df = df.sample(frac=1)
        ds_s = df_s.values
        
        in_ds_s = ds_s[:,1:13]
        out_ds_s = ds_s[:,13]
        
        model = self._model_c()    
        model.fit(in_ds_s, out_ds_s, epochs=epochs, batch_size=batch_size)
        model.model.save('models\\' + model_name + '.hdf5')
        
        self.model = model
    
    def load_model(model_name: str) -> KerasRegressor:
        
        def dummy():
            return
        model = KerasRegressor(build_fn=dummy, epochs=1, batch_size=10, verbose=1)
        model.model = ld_mdl('models\\' + model_name + '.hdf5')
        
        return model
    
    def test_model(self, bm_id_list: list, model_name: str):
        
        if (self.model == None):
            print("No model loaded, either train one or load one")
            return False
        
        rating_list = []
        log = []
        
        # Check if plot path is valid
        try:
            # Create target Directory
            os.mkdir(self.plot_dir)
            print("Plot Directory Created: " + self.plot_dir)
        except FileExistsError:
            print("Plot Directory Exists: " + self.plot_dir)
            
        
        for bm_id in bm_id_list:
            ppshift_f = open(self.ppshift_dir + str(bm_id) + '.ppshift', 'r')
            # Important: The first 29 results has a 0 output, so we will cut
            # those results out with splicing.
            # This is due to the rolling Aggregation
            ppshift_str = ppshift_f.read().splitlines()[29:]
            ppshift_f.close()
            
            ppshift_df = pandas.DataFrame(list(map(eval, ppshift_f)))
            
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
            plt.savefig(self.plot_dir + title + '.jpg')
            # Do not display plot in IPython console
            plt.close()
            
            # RATE PLOTS
            out['delta'] = out['pred'].subtract(out['original']).abs()
            log.append(str(out['delta'].mean()) + "\t" + \
                       get_beatmap_metadata.metadata_from_id([b_id])['metadata'].values[0])
    
            rating_list.append(out['delta'].mean())
            
        log.append("mean: " + str(statistics.mean(rating_list)))
        log.append("stdev: " + str(statistics.stdev(rating_list)))
        
        log_f = open(self.plot_dir + "results.txt", "w+")
        log_f.write('\n'.join(log))
        
# =============================================================================
#     def random_test_model(maps_to_test: int, model_name: str):
#             
#         files = list(map(int, [x.split('.')[0] for x in os.listdir(save_to.dirs.dir_ppshift)[0:-1]]))
#         # We will filter out < 5 star rating
#         files_filter = get_beatmap_metadata.get_id_by_filters(5.0)  
#         files = list(filter(lambda x : x in files_filter, files))     
#         random_list = random.sample(files, maps_to_test)
#         
#         test_model(load_model(model_name), random_list, model_name)
#     
#     model_name = "e25_96_48_24_100"
#     
#     # merge_df(0.8)
#     train_model(model_name,0.5,25)
#     random_test_model(121, model_name)
#     #test_model( load_model("two_layer"), [1505212], "two_layer_plots")
# =============================================================================
