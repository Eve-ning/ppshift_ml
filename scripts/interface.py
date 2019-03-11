# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 13:13:08 2019

@author: user
"""

import pandas

# =============================================================================
# import api_main
# import api_main_beatmap_id_data
# import api_main_plyrid
# import api_main_plyrid_to_acr
#
# import download_difficulties
#
# import from_acd_to_ppshift
# import from_acr_to_acrv
# import from_osu_to_osus
# import from_osus_to_acd
#
# import get_beatmap_metadata
# import save_to
# =============================================================================

def get_keys(beatmap_id: int) -> bool:
def get_beatmap_from_website(beatmap_id: int) -> bool:
    return
def get_plyrid(beatmap_id: int) -> bool:
    return
def get_acr_from_plyrid(beatmap_id: int) -> bool:
    return
def convert_osu_to_osus(beatmap_id: int) -> bool:
    return
def convert_osuho_to_acd(beatmap_id: int) -> bool:
    is_special_style()
    return
def is_special_style(beatmap_id: int) -> bool:
    return
def is_scroll_change_valid(beatmap_id: int) -> bool:
    
    return
def append_to_pkl(series: pandas.Series):

    print("<Insert Metadata>")
    input("Is scroll change valid: [y/n]")
    # User will manually decide if new osu has a valid scroll change

    return

def parse_osu(beatmap_id: int) -> bool:

    success_flag = True

# =============================================================================
#   API -> .osu
#   Firstly, we need to download the .osu from the website
#   We check if it's downloaded already, and skip if it's already done
#   Download into /osu/ folder
#
#   We are only training the beatmaps here, if they are not on the server
#   this means we don't have replays for it, so it's impossible to train them
# =============================================================================
    success_flag = get_beatmap_from_website(beatmap_id)
    if (success_flag):
        print()
    else:
        print()

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
    convert_osu_to_osus(beatmap_id)
    if (success_flag):
        print()
    else:
        print()

# =============================================================================
#   filter: scroll_change_filter
#   If the scroll change is not valid, we will reject this input
# =============================================================================
    if(is_scroll_change_valid(beatmap_id)):
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
    convert_osuho_to_acd(beatmap_id)

# =============================================================================
#   API -> .plyrid
#   Similar to downloading .osu, we get the .plyrid list 
#   FORMAT: <rank>, <player_id>
#   Download into /plyrid/ folder
# =============================================================================
    get_plyrid(beatmap_id)
    
# =============================================================================
#   .plyrid -> .acr
#   For this function, we will need to map the columns to the actual
#   fingering of the key_count
#   Grabs the acr from the plyrid list
#   If replay download fails, we append a dummy
#   FORMAT: <offset>, <action>
# =============================================================================
    get_acr_from_plyrid(beatmap_id)
    
# =============================================================================
#   .acr + .acd -> .acrv
#   Matches the acr to acd
#   Merges the acr by getting the median
#   FORMAT: 
# =============================================================================

    # .acd + .acrv -> .ppshift
    # 
    # .ppshift -> .pkl

    # .pkl -> merge

    # merge -> train -> .hdf5

    # .acd + .hdf5 -> pred
