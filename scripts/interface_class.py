# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 15:30:55 2019

@author: user
"""
import pandas


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
    def __init__(self, beatmap_id):
        self.beatmap_id = beatmap_id
        
    self.beatmap_id: int
    
    # Grab from settings
    keys: int
    is_special_style: bool
    
    # User Input
    is_scroll_change_valid: bool
    
    # default osu format
    osu: str
    
    # vector<initial_offset, end_offset, column>
    osuho: pandas.DataFrame
    
    # vector<initial_offset, value, is_bpm>
    osutp: pandas.DataFrame
    
    # vector<action_offset>
    acd: pandas.DataFrame
    
    # 50 Replays
    # vector<vector<action_offset>>
    acr: pandas.DataFrame
    
    # 1 Replay
    # vector<action_offset>
    acrv: pandas.DataFrame
    
    metadata: dict = {
            'keys': None,
            'title': None,
            'artist': None,
            'creator': None,
            'version': None
            }
    
    def get_beatmap_metadata(self) -> str:
        metadata_str = \
        self.metadata['artist'] + ' - ' + \
        self.metadata['title'] + ' (' + \
        self.metadata['version'] + ') <' + \
        self.metadata['creator'] + '>'
        
        return metadata_str
    
    def get_beatmap_from_website(self) -> bool:
        return
    def get_plyrid(self) -> bool:
        return
    def plyrid_to_acr(self) -> bool:
        return
    def osu_to_osus(self) -> bool:
        return
    def osus_to_acd(self) -> bool:
        return
    def acr_to_acrv(self) -> bool:
        return
    def ac_to_ppshift(self) -> bool:
        return

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
            self.osu = self.get_beatmap_from_website(self)
        
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
            self.osuho, self.osutp = self.osu_to_osus(self)
        
# =============================================================================
#   filter: scroll_change_filter
#   If the scroll change is not valid, we will reject this input
# =============================================================================
            
        if(self.is_scroll_change_valid == None):
            # User will manually decide if new osu has a valid scroll change
            print(self.get_beatmap_metadata())
            input("Is scroll change valid: [y/n]")
        
        if(not self.is_scroll_change_valid):
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
            
        self.acd = self.osus_to_acd(self)
    
# =============================================================================
#   API -> .plyrid
#   Similar to downloading .osu, we get the .plyrid list 
#   FORMAT: <rank>, <player_id>
#   Download into /plyrid/ folder
# =============================================================================
        
        self.plyrid = self.get_plyrid(self)
        
# =============================================================================
#   .plyrid -> .acr
#   For this function, we will need to map the columns to the actual
#   fingering of the key_count
#   Grabs the acr from the plyrid list
#   If replay download fails, we append a dummy
#   FORMAT: <offset>, <action>
# =============================================================================
        
        self.acr = self.plyrid_to_acr(self)
        
# =============================================================================
#   .acr + .acd -> .acrv
#   Matches the acr to acd
#   Merges the acr by getting the median
#   FORMAT: 
# =============================================================================
    
        self.acrv = self.get_
    
# =============================================================================
#   .acd + .acrv -> .ppshift
#   Gets all required parameters from the beatmap and replay to prepare
#   for neural network learning
# =============================================================================
        # 
        # .ppshift -> .pkl
    
        # .pkl -> merge
    
        # merge -> train -> .hdf5
    
        # .acd + .hdf5 -> pred
    
    
    
    