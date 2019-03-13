# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 15:30:55 2019

@author: user
"""
import pandas

# import api_main
# import api_main_beatmap_id_data

# import from_acd_to_ppshift
# import from_acr_to_acrv

import get_osu_from_website
import osu_to_osus
import osuho_to_acd
import get_plyrid
import plyrid_to_acr
import ac_to_acrv
import ac_to_ppshift

import interface_io

class beatmap:
    
    def __init__(self, beatmap_id: int):
        self.beatmap_id = beatmap_id
                
        self.io = interface_io.interface_io(beatmap_id)
        
        self.osu = self.io.load('osu')
        if (self.osu):
            self.osu = self.osu.splitlines()
        
        self.osuho = self.io.load('osuho')
        if (self.osuho):
            self.osuho = list(map(eval, self.osuho.splitlines()))
        
        self.osutp = self.io.load('osutp')
        if (self.osutp):
            self.osutp = list(map(eval, self.osutp.splitlines()))
        
        self.acd = self.io.load('acd')
        if (self.acd):
            self.acd = list(map(eval, self.acd.splitlines()))

        self.plyrid = self.io.load('plyrid')
        if (self.plyrid):
            self.plyrid = list(map(eval, self.plyrid.splitlines()))
        
        self.acr = self.io.load('acr')
        if (self.acr):
            self.acr = list(map(eval, self.acr.splitlines()))

        self.acrv = self.io.load('acrv')
        if (self.acrv):
            self.acrv = list(map(eval, self.acrv.splitlines()))

        self.ppshift = self.io.load('ppshift')
        if (self.ppshift):
            self.ppshift = list(map(eval, self.osutp.splitlines()))
        
        self.params = self.io.load('params')
        if (self.params):
            self.params = eval(self.params)

        if (self.params == None):
            self.params = {}

        
    def get_beatmap_metadata(self) -> str:
        metadata_str = \
        self.params['artist'] + ' - ' + \
        self.params['title'] + ' (' + \
        self.params['version'] + ') <' + \
        self.params['creator'] + '>'
        
        return metadata_str
    
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
        
        print("[OSU]", end=' ')
        if (self.osu == None):
            self.osu = get_osu_from_website.run(self.beatmap_id)

            if (self.osu == None):
                raise AssertionError('Fail to get .osu from website')
            
            self.io.save('osu', '\n'.join(self.osu), True)
            print("[CREATED]")
        else:
            print("[EXISTS]")
        
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

        print("[OSUS]", end=' ')
        if ((self.osuho == None) or (self.osutp == None)):
            self.osuho, self.osutp, \
            self.params['keys'], \
            self.params['title'], \
            self.params['artist'], \
            self.params['creator'], \
            self.params['version'], \
            self.params['special_style'] = \
            osu_to_osus.run(self.osu)
            
            if (self.osuho == None):
                raise AssertionError('Fail to read Hit Object from .osu')
            elif (self.osutp == None):
                raise AssertionError('Fail to read Timing Point from .osu')
            elif (self.params['keys'] == None):
                raise AssertionError('Fail to read Keys from .osu')
            elif (self.params['title'] == None):
                raise AssertionError('Fail to read Title from .osu')
            elif (self.params['artist'] == None):
                raise AssertionError('Fail to read Artist from .osu')
            elif (self.params['creator'] == None):
                raise AssertionError('Fail to read Creator from .osu')
            elif (self.params['version'] == None):
                raise AssertionError('Fail to read Version from .osu')
            elif (self.params['special_style'] == None):
                raise AssertionError('Fail to read Special Style from .osu')
            
            osuho_str = '\n'.join(list(map(str, self.osuho)))
            osutp_str = '\n'.join(list(map(str, self.osutp)))
            self.io.save('osuho', osuho_str, True)
            self.io.save('osutp', osutp_str, True)
            
            # Even though reject is None
            # we will save the params just in case of error
            self.io.save('params', str(self.params), True)
            print("[CREATED]")
        else:
            print("[EXISTS]")

# =============================================================================
#   filter: scroll_change_filter
#   If the scroll change is not valid, we will reject this input
# =============================================================================
        print("[PARAMS]", end=' ')           
        if ('reject' not in self.params):
            # User will manually decide if new osu has a valid scroll change
            print(self.get_beatmap_metadata())
            user_input = ''
            while (user_input != 'y' and user_input != 'n'):
                user_input = input("Reject Map [y/n]: ")
                
            if (user_input == 'y'): # for 'y'
                self.params['reject'] = True
                
                user_input_reason = ""
                reject_reason_dic = {
                        "1": "Scroll Speed Changes",
                        "2": "Not enough Scores",
                        "3": "Broken beatmap",
                        "4": "Others"
                        }
                
                # This is where a specific reason is specified
                while (user_input_reason != "1" and \
                       user_input_reason != "2" and \
                       user_input_reason != "3" and \
                       user_input_reason != "4"):
                    
                    print(reject_reason_dic)
                    user_input_reason = \
                    input("Reason for rejection: ")
                    
                self.params['reject_reason'] = \
                reject_reason_dic[user_input_reason]
                    
                # This is a broad reason
                if (user_input_reason == "4"):
                    self.params['reject_reason'] = \
                    input("Details of rejection: ")
                
            else: # for 'n'
                self.params['reject'] = False
            
            # This will complete the save_pkl for params
            self.io.save('params', str(self.params), True)
            print("[CREATED]")
        else:
            print("[EXISTS]")
            
        if (self.params['reject']):
            print("[REJECTED]: {rsn}".format(rsn = self.params['reject_reason']))
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

        print("[ACD]", end=' ')
        if (self.acd == None):
            self.acd = osuho_to_acd.run(self.osuho, self.params['keys'])
            if (self.acd == None):
                raise AssertionError('Fail to convert Hit Objects to Action Difficulty')
            
            acd_str = '\n'.join(list(map(str, self.acd)))
            
            self.io.save('acd', acd_str, True)
            print("[CREATED]")
        else:
            print("[EXISTS]")
            
# =============================================================================
#   API -> .plyrid
#   Similar to downloading .osu, we get the .plyrid list 
#   FORMAT: <rank>, <player_id>
#   Download into /plyrid/ folder
# =============================================================================
        
        print("[PLYRID]", end=' ')
        if (self.plyrid == None):
            self.plyrid = get_plyrid.run(self.beatmap_id)
            if (self.plyrid == None):
                raise AssertionError('Fail to get Player IDs from Beatmap ID')
            self.io.save('plyrid', '\n'.join(self.plyrid), True)      
            print("[CREATED]")
        else:
            print("[EXISTS]")
            
# =============================================================================
#   .plyrid -> .acr
#   For this function, we will need to map the columns to the actual
#   fingering of the key_count
#   Grabs the acr from the plyrid list
#   If replay download fails, we append a dummy
#   FORMAT: <offset>, <action>
# =============================================================================
        
        print("[ACR]", end=' ')
        if (self.acr == None):
            print()
            self.acr = plyrid_to_acr.run(self.plyrid, self.beatmap_id, self.params['keys'])
            if (self.acr == None):
                raise AssertionError('Fail to convert Player IDs to Action Replay')
            
            acr_list = []
            for replay in self.acr:
                acr_list.append(str(list(map(str, replay))))
                
            # We will remove any quotes 
            acr_str = '\n'.join(acr_list) \
                          .replace("'","") \
                          .replace("[[","[") \
                          .replace("]]","]")
            
            self.io.save('acr', acr_str, True)   
            print("[CREATED]")
        else:
            print("[EXISTS]")

    
# =============================================================================
#   .acr + .acd -> .acrv
#   Matches the acr to acd
#   Merges the acr by getting the median
#   FORMAT: 
# =============================================================================
        
        print("[ACRV]", end=' ')
        if (self.acrv == None):
            self.acrv = ac_to_acrv.run(self.acr, self.acd)
            if (self.acrv == None):
                raise AssertionError('Fail to convert Actions to Action Replay Virtual')
                
            acrv_str = '\n'.join(list(map(str, self.acrv)))
                
            self.io.save('acrv', acrv_str, True)   
            print("[CREATED]")
        else:
            print("[EXISTS]")
            
# =============================================================================
#   .acd + .acrv -> .ppshift
#   Gets all required parameters from the beatmap and replay to prepare
#   for neural network learning
# =============================================================================
        print("[PPSHIFT]", end=' ')
        if (self.ppshift == None):
            self.ppshift = ac_to_ppshift.run(self.acd, self.acrv)
            if (self.ppshift == None):
                raise AssertionError('Fail to convert Actions to PPShift')
            print(self.ppshift)
            # self.io.save('ppshift', '\n'.join(self.ppshift), True)   
            print("[CREATED]")
        else:
            print("[EXISTS]")
            
# =============================================================================
#   End    
# =============================================================================
        return True

    
    
bm = beatmap(1104774)
bm.parse_osu()


    