# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 15:30:55 2019

@author: user
"""
import pandas

import api_main
import api_main_beatmap_id_data
import api_main_plyrid
import api_main_plyrid_to_acr

import download_difficulties

import from_acd_to_ppshift
import from_acr_to_acrv
import osu_to_osus
import from_osus_to_acd

import get_osu_from_website
import save_to
import interface_io


column_to_action = {
    4: [2,3,5,6],
    5: [2,3,4,5,6],
    6: [1,2,3,5,6,7],
    7: [1,2,3,4,5,6,7],
    8: [0,1,2,3,5,6,7,8],
    9: [0,1,2,3,4,5,6,7,8],
}

def to_action(self, offset:float, keys:int, column:int):
    return column_to_action[keys][column]

class beatmap:
    def __init__(self, beatmap_id: int):
        self.osu = interface_io.load_pkl(self.params['beatmap_id'], 'osu')
            
        # vector<initial_offset, end_offset, column>
        self.osuho = interface_io.load_pkl(self.params['beatmap_id'], 'osuho')
        
        # vector<initial_offset, value, is_bpm>
        self.osutp = interface_io.load_pkl(self.params['beatmap_id'], 'osutp')
        
        # vector<offset, action>
        self.acd = interface_io.load_pkl(self.params['beatmap_id'], 'acd')
        
        # 50 Replays
        # vector<vector<offset, action>>
        self.acr = interface_io.load_pkl(self.params['beatmap_id'], 'acr')
        
        # 1 Replay
        # vector<offset, action>
        self.acrv = interface_io.load_pkl(self.params['beatmap_id'], 'acrv')
        
        # vector<neural_network_parameters>
        self.ppshift = interface_io.load_pkl(self.params['beatmap_id'], 'ppshift')
        
        self.params = interface_io.load_pkl(self.params['beatmap_id'], 'params')
        
        #  dict = {
        #         'keys': None,
        #         'title': None,
        #         'artist': None,
        #         'creator': None,
        #         'version': None,
        #         'beatmap_id': beatmap_id,
        
        #         # Grab from settings
        #         'special_style': None,
                
        #         # User Input
        #         'is_scroll_change_valid': None
        #         }

    def get_beatmap_metadata(self) -> str:
        metadata_str = \
        self.params['artist'] + ' - ' + \
        self.params['title'] + ' (' + \
        self.params['version'] + ') <' + \
        self.params['creator'] + '>'
        
        return metadata_str
    

    @classmethod
    def parse_osu(self) -> bool:

# =============================================================================
#   API -> .osu
#   Firstly, we need to download the .osu from the website
#   We check if it's downloaded already, and skip if it's already done
#   Download into /osu/ folder
# 
#   We are only training the beatmaps here, if they are not on the server
#   this means we don't have replays for it, so it's impossible to
#   train them
# =============================================================================
        
        if (self.osu == None):
            self.osu = get_osu_from_website.run(self.params['beatmap_id'])
            interface_io.save_pkl(self.params['beatmap_id'], self.osu, 'osu')
        
# =============================================================================
#   .osu -> .osuho + .osutp
#   Extract all relevant information from the .osu file
#
#   Hit Object -> .osuho
#   FORMAT: <initial_offset>, <end_offset>, <column>
#
#   Timing Point -> .osutp
# 	FORMAT: <initial_offset>, <value>, <is_bpm>
#
#   General Data -> append to .pkl as metadata for each id
# =============================================================================
    
        if (self.osuho == None or self.osutp == None):
            self.osuho, self.osutp, \
            self.params['keys'], \
            self.params['title'], \
            self.params['artist'], \
            self.params['creator'], \
            self.params['version'], \
            self.params['special_style'] = \
            osu_to_osus(self.osu)
            
            interface_io.save_pkl(self.params['beatmap_id'], self.osuho, 'osuho')
            interface_io.save_pkl(self.params['beatmap_id'], self.osutp, 'osutp')
            
            # Even though is_scroll_change_valid is None
            # we will save the params just in case of error
            interface_io.save_pkl(self.params['beatmap_id'], self.params, 'params')
        
# =============================================================================
#   filter: scroll_change_filter
#   If the scroll change is not valid, we will reject this input
# =============================================================================
            
        if (self.params['is_scroll_change_valid'] == None):
            # User will manually decide if new osu has a valid scroll change
            print(self.get_beatmap_metadata())
            user_input = ''
            while (user_input != 'y' or user_input != 'n'):
                user_input = input("Is scroll change valid: [y/n]")
            if (user_input == 'y'):
                self.params['is_scroll_change_valid'] = True
            else: # for 'n'
                self.params['is_scroll_change_valid'] = False
            
            # This will complete the save_pkl for params
            interface_io.save_pkl(self.params['beatmap_id'], self.params, 'params')
            
        if (not self.params['is_scroll_change_valid']):
            # Halt all calculations if scroll change is not valid
            return
    
# =============================================================================
#   .osuho -> .acd
#   For this function, we will need to map the columns to the actual
#   fingering of the key_count
#   This will group by offset
#   FORMAT: <offset>, <action>
#   For the keys,
#       X = press key X,
#       -X = release key X,
#       0 = nothing
# =============================================================================
        
        if (self.acd == None):
            self.acd = osuho_to_acd(self.osuho, self.params['is_scroll_change_valid'])
            interface_io.save_pkl(self.params['beatmap_id'], self.acd, 'acd')
            
# =============================================================================
#   API -> .plyrid
#   Similar to downloading .osu, we get the .plyrid list 
#   FORMAT: <rank>, <player_id>
#   Download into /plyrid/ folder
# =============================================================================
        
        if (self.plyrid == None):
            self.plyrid = get_plyrid(self.params['beatmap_id'])
            interface_io.save_pkl(self.params['beatmap_id'], self.plyrid, 'plyrid')      
            
# =============================================================================
#   .plyrid -> .acr
#   For this function, we will need to map the columns to the actual
#   fingering of the key_count
#   Grabs the acr from the plyrid list
#   If replay download fails, we append a dummy
#   FORMAT: <offset>, <action>
# =============================================================================
        
        if (self.acr == None):
            self.acr = self.plyrid_to_acr(self.plyrid)
            interface_io.save_pkl(self.params['beatmap_id'], self.acr, 'acr')   
            
# =============================================================================
#   .acr + .acd -> .acrv
#   Matches the acr to acd
#   Merges the acr by getting the median
#   FORMAT: 
# =============================================================================
    
        if (self.acrv == None):
            self.acrv = ac_to_acrv(self.acr, self.acd)
            interface_io.save_pkl(self.params['beatmap_id'], self.acrv, 'acrv')   
            
# =============================================================================
#   .acd + .acrv -> .ppshift
#   Gets all required parameters from the beatmap and replay to prepare
#   for neural network learning
# =============================================================================
        
        if (self.ppshift == None):
            self.ppshift = ac_to_ppshift(self.acrv, self.acd)
            interface_io.save_pkl(self.params['beatmap_id'], self.ppshift, 'ppshift')   
            
# =============================================================================
#   End    
# =============================================================================
        return True

    
        # merge -> train -> .hdf5
    
        # .acd + .hdf5 -> pred
    
        



    