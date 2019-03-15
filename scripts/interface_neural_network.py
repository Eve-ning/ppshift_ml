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
import numpy
import matplotlib.pyplot as plt
import random
import re
import statistics

class train_model:
    
    def __init__(self, model_name: str, seed: int = None, training_split: float = 0.8):
        
        # Randomize if seed is not provided
        if (seed != None):
            random.seed(seed)

        self.ppshift_dir = "D:\\Data Documents\\ppshift\\ppshift_ml\\documents\\ppshift\\"
        self.plot_dir = "D:\\Data Documents\\ppshift\\ppshift_ml\\documents\\neural_network\\plots\\" + \
                        model_name + "\\"
        self.model_dir = "D:\\Data Documents\\ppshift\\ppshift_ml\\documents\\neural_network\\models\\"
        
        # We will define training and test split here
        # This converts all of them into int after listing them
        files = list(map(int, \
                         [x.split('.')[0] for x in os.listdir(self.ppshift_dir)]))
    
        random.shuffle(files) # We will randomly shuffle it
        training_len = int(len(files) * training_split)
        
        self.training_ids = files[:training_len]
        self.testing_ids = files[training_len:]
        self.model_name = model_name
        self.model = None
    
    def train(self, epochs: int, batch_size: int):
        self._load_training()
        self._train_model(epochs, batch_size)
    
    def _load_training(self): 
             
        print("Merging " + str(len(self.training_ids)) + " files")
        print(self.training_ids)
    
        ppshift_list = []
        
        for bm_id in self.training_ids:
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
        
        model = keras.Sequential()
        
        self.layer_1_nrns = 96
        self.layer_2_nrns = None
        self.layer_3_nrns = None
        
        model.add(keras.layers.Dense(self.layer_1_nrns, input_shape=(12,), \
                                     kernel_initializer='normal', \
                                     activation='relu'))
        if (self.layer_2_nrns != None):
            model.add(keras.layers.Dense(self.layer_2_nrns,\
                                         kernel_regularizer=keras.regularizers.l2(0.01)))
        if (self.layer_3_nrns != None):
            model.add(keras.layers.Dense(self.layer_3_nrns,\
                                         kernel_regularizer=keras.regularizers.l2(0.01)))
        model.add(keras.layers.Dense(1, kernel_initializer='normal'))
    
        model.compile(loss='mean_squared_error', optimizer='adam')
        
        return model
    
    def _train_model(self, epochs: int, batch_size: int):
        
        df = self.training_df 

        # Shuffle
        df = df.sample(frac=1)
        ds_s = df.values
        
        in_ds_s = ds_s[:,1:13]
        out_ds_s = ds_s[:,13]
        
        model = self._model_c()    
        model.fit(in_ds_s, out_ds_s, epochs=epochs, batch_size=batch_size)
        
        # Save model
        model.model.save(self.model_dir + self.model_name + '.hdf5')
        
        self.model = model
        
    def test(self):
        self._load_model()
        self._test_model(self.testing_ids, 'results_tst')
        self._test_model(self.training_ids, 'results_trn')
        
    def _load_model(self):
        
        def dummy():
            return
        model = KerasRegressor(build_fn=dummy, epochs=1, batch_size=10, verbose=1)
        model.model = ld_mdl(self.model_dir + self.model_name + '.hdf5')
        
        self.model = model
    
    def _test_model(self, bm_ids, log_file_name = 'results'):
        
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
            
        
        for bm_id in bm_ids:
            ppshift_f = open(self.ppshift_dir + str(bm_id) + '.ppshift', 'r')
            # Important: The first 29 results has a 0 output, so we will cut
            # those results out with splicing.
            # This is due to the rolling Aggregation
            ppshift_str = ppshift_f.read().splitlines()[29:]
            ppshift_f.close()
            
            ppshift_df = pandas.DataFrame(list(map(eval, ppshift_str)))
            
            ds = ppshift_df.values
            
            in_ds = ds[:,1:13]
            out_ds = ds[:,[0,13]]
            
            out_p = self.model.predict(in_ds, verbose=0)
            
            out_o = pandas.DataFrame(out_ds, columns=['offset','original'])
            out_p = pandas.DataFrame(out_p, columns=['pred'])
            
            out = out_o.join(out_p)
            
            # CREATE PLOTS
            title = get_beatmap_metadata.metadata_from_id(int(bm_id))
            title = re.sub('[^\w_.)( -]', '', title)
            out.plot(x='offset', title=title)
            
            # Save plot
            plt.savefig(self.plot_dir + title + '.jpg')
            # Do not display plot in IPython console
            plt.close()
            
            perc_15 = numpy.percentile(out_p, 15)
            perc_25 = numpy.percentile(out_p, 25)
            perc_50 = numpy.percentile(out_p, 50)
            perc_75 = numpy.percentile(out_p, 75)
            perc_85 = numpy.percentile(out_p, 85)
            
            # RATE PLOTS
            out['delta'] = out['pred'].subtract(out['original']).abs()
            log.append(str(out['delta'].mean()) + "\t" + \
                       get_beatmap_metadata.metadata_from_id(int(bm_id)) + \
                       str(perc_15) + '\t' + \
                       str(perc_25) + '\t' + \
                       str(perc_50) + '\t' + \
                       str(perc_75) + '\t' + \
                       str(perc_85))
    
            rating_list.append(out['delta'].mean())
            
        # Append stats
        log.append("mean: " + str(statistics.mean(rating_list)))
        log.append("stdev: " + str(statistics.stdev(rating_list)))
        log.append("range: " + str(min(rating_list)) + ' - ' \
                   + str(max(rating_list))) 
        
        print(log_file_name)
        print(log[-3])
        print(log[-2])
        print(log[-1])
        
        log_f = open(self.plot_dir + log_file_name + ".txt", "w+")
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

    def evaluate(self):
        print()
        
    def _eval_model(self, file_path, log_file_name = 'results'):
        print()
        
class eval_model:
    
    def __init__(self, model_name: str):
        self.plot_dir = "D:\\Data Documents\\ppshift\\ppshift_ml\\documents\\eval\\plots\\" + \
                        model_name + "_eval\\"
        self.model_dir = "D:\\Data Documents\\ppshift\\ppshift_ml\\documents\\neural_network\\models\\"
        self.ppshift_dir = "D:\\Data Documents\\ppshift\\ppshift_ml\\documents\\eval\\ppshift\\"
        # self.csv_path = self.plot_dir + "results.csv"
        # self.results = pandas.read_csv()
        self.model_name = model_name
        self.model = None
        
    def evaluate(self):
        self._load_model()
        file_names = [x.split('.')[0] for x in os.listdir(self.ppshift_dir)]
        self._eval_model(file_names)
        
    def _load_model(self):
        
        def dummy():
            return
        model = KerasRegressor(build_fn=dummy, epochs=1, batch_size=10, verbose=1)
        model.model = ld_mdl(self.model_dir + self.model_name + '.hdf5')
        
        self.model = model
        return 
    
    def _eval_model(self, file_names):
        
        if (self.model == None):
            print("No model loaded, either train one or load one")
            return False
        
        # rating_list = []
        # log = []
        
        # Check if plot path is valid
        try:
            # Create target Directory
            os.mkdir(self.plot_dir)
            print("Plot Directory Created: " + self.plot_dir)
        except FileExistsError:
            print("Plot Directory Exists: " + self.plot_dir)
            
        
        for file_name in file_names:
            
            title = file_name
            title = re.sub('[^\w_.)( -]', '', title)
            
            if (os.path.isfile(self.plot_dir + title + '.jpg')):
                print(file_name + " exists, skipping.")
                continue
            
            ppshift_f = open(self.ppshift_dir + file_name + '.ppshift', 'r')
            # Important: The first 29 results has a 0 output, so we will cut
            # those results out with splicing.
            # This is due to the rolling Aggregation
            ppshift_str = ppshift_f.read().splitlines()[29:]
            ppshift_f.close()
            
            ppshift_df = pandas.DataFrame(list(map(eval, ppshift_str)),\
                                          columns=['offset','LP','LR','LM','LI','S', \
                                                   'RI','RM','RR','RP','NN','LNH','LNT'])
            
            ds = ppshift_df.values
            
            in_ds = ds[:,1:13]
            
            out_p = self.model.predict(in_ds, verbose=0)

            out_p = pandas.DataFrame(out_p, columns=['predict'])
            
            out = ppshift_df.join(out_p)
            
            # CREATE PLOTS

            out.plot(x='offset', y='predict', title=title)
            
            # Save plot
            plt.savefig(self.plot_dir + title + '.jpg')
            # Do not display plot in IPython console
            plt.close()
            
            # # RATE PLOTS
            # out['delta'] = out['pred'].subtract(out['original']).abs()
            # log.append(str(out['delta'].mean()))
    
            # rating_list.append(out['delta'].mean())
            # log_f = open(self.plot_dir + log_file_name + ".txt", "w+")
            # log_f.write('\n'.join(log))
            
