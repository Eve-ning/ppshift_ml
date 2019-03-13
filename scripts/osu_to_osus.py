# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 18:13:05 2019

@author: user
"""

# returns offset, value, is_bpm
def read_timing_point(tp: str):
    tp_list = tp.split(",")
    offset = int(round(float(tp_list[0])))
    value = (60000.0 if tp_list[6] == '1' else -100.0) / float(tp_list[1])
    
    return [offset, value, tp_list[6] == '1']
    
# returns offset, offset_end(0 if normal note), column
def read_hit_object(ho: str, keys: int):       
    ho_list = ho.split(",")
    offset = int(ho_list[2])
    offset_end = int(ho_list[5].split(":")[0]) if ho.count(":") == 5 else 0
    column = round((int(ho_list[0]) * keys - 256)/512) + 1
    
    return [offset, offset_end, column]

# We take a beatmap_id as an input
# We will create a separate file format for easier reading
def run(osu: list):
    
    osu = list(filter(lambda x : len(x) != 0, osu))

    special_style = None
    
    title = None
    artist = None
    creator = None
    version = None
    
    keys = None

    tp_list = []
    ho_list = []
    
    counter = 0
    
# =============================================================================
#     # Find Params
# =============================================================================
    
    while (not "TimingPoints" in osu[counter]) and counter < len(osu):
        
        if (osu[counter].startswith("SpecialStyle:")):
            special_style = (osu[counter].split(":")[1].strip() == '1')
            
        elif (osu[counter].startswith("Title:")):
            title = osu[counter].split(":")[1].strip()
            
        elif (osu[counter].startswith("Artist:")):
            artist = osu[counter].split(":")[1].strip()
            
        elif (osu[counter].startswith("Creator:")):
            creator = osu[counter].split(":")[1].strip()
            
        elif (osu[counter].startswith("Version:")):
            version = osu[counter].split(":")[1].strip()
            
        elif (osu[counter].startswith("CircleSize:")):
            keys = int(osu[counter].split(":")[1]) # Circle Size will always be 1 digit
        
        counter += 1

    # Skip Tag
    counter += 1
    
# =============================================================================
#     # Reach [TimingPoints]
# =============================================================================
    
    while (not "HitObjects" in osu[counter]) and counter < len(osu):
        
        # Append for all Timing Point
        if (osu[counter][0].isdigit()):
            tp_list.append(read_timing_point(osu[counter]))
        
        counter += 1
            
    # Skip Tag
    counter += 1
    
# =============================================================================
#     # Reach [HitObject]
# =============================================================================
    
    while counter < len(osu):
        
        # Append for all Hit Object
        if (osu[counter][0].isdigit()):
            ho_list.append(read_hit_object(osu[counter], keys))
            
        counter += 1
    
    return ho_list, tp_list, keys, title, artist, creator, version, special_style
    
# =============================================================================
# osu file format v13
# 
# [General]
# AudioFilename: Terekakushi Shishunki.mp3
# AudioLeadIn: 0
# PreviewTime: 61069
# Countdown: 0
# SampleSet: Soft
# StackLeniency: 0.6
# Mode: 3
# LetterboxInBreaks: 0
# SpecialStyle: 0
# WidescreenStoryboard: 1
# 
# [Editor]
# DistanceSpacing: 0.9
# BeatDivisor: 4
# GridSize: 32
# TimelineZoom: 2.2
# 
# [Metadata]
# Title:Terekakushi Shishunki
# TitleUnicode:テレカクシ思春期
# Artist:Sana
# ArtistUnicode:鎖那
# Creator:Rumia-
# Version:Insane
# Source:
# Tags:HoneyWorks nico_nico_douga shito hidden shy puberty [shi-ra] cover
# BeatmapID:320196
# BeatmapSetID:125877
# 
# [Difficulty]
# HPDrainRate:8
# CircleSize:7
# OverallDifficulty:8
# ApproachRate:5
# SliderMultiplier:1.4
# SliderTickRate:1
# =============================================================================