# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 15:30:55 2019

@author: user
"""

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

class parse_beatmap_id:
    
    def __init__(self, beatmap_id: int, soft_load_flag=False):
        
        self.beatmap_id = beatmap_id
        self.soft_load_flag = soft_load_flag
                
        self.io = interface_io.interface_io(beatmap_id)
        
        # Soft load only gets the file's existence
        # This is much faster to check if it's done
        self.soft_load()
        
        # Hard load evaluates the file
        if (not soft_load_flag):
            self.hard_load()
            
        # We will load params anyway, it's not slow
        self.params = self.io.load('params')
        if (self.params):
            self.params = eval(self.params)
        if (self.params == None):
            self.params = {}

    def soft_load(self):
        self.osu = self.io.exist('osu')
        self.osuho = self.io.exist('osuho')
        self.osutp = self.io.exist('osutp')
        self.acd = self.io.exist('acd')
        self.plyrid = self.io.exist('plyrid')
        self.acr = self.io.exist('acr')
        self.acrv = self.io.exist('acrv')
        self.ppshift = self.io.exist('ppshift')

    def hard_load(self):
        self.soft_load_flag=False
        
        self.osu = self.io.load('osu')
        self.osuho = self.io.load('osuho')
        self.osutp = self.io.load('osutp')
        self.acd = self.io.load('acd')
        self.plyrid = self.io.load('plyrid')
        self.acr = self.io.load('acr')
        self.acrv = self.io.load('acrv')
        self.ppshift = self.io.load('ppshift')
        
        if (self.osu):
            self.osu = self.osu.splitlines()
        if (self.osuho):
            self.osuho = list(map(eval, self.osuho.splitlines()))
        if (self.osutp):
            self.osutp = list(map(eval, self.osutp.splitlines()))
        if (self.acd):
            self.acd = list(map(eval, self.acd.splitlines()))
        if (self.plyrid):
            self.plyrid = list(map(eval, self.plyrid.splitlines()))
        if (self.acr):
            self.acr = list(map(eval, self.acr.splitlines()))
        if (self.acrv):
            self.acrv = list(map(eval, self.acrv.splitlines()))
        if (self.ppshift):
            self.ppshift = list(map(eval, self.ppshift.splitlines()))  
     
    def get_beatmap_metadata(self) -> str:
        try:
            metadata_str = \
            self.params['artist'] + ' - ' + \
            self.params['title'] + ' (' + \
            self.params['version'] + ') <' + \
            self.params['creator'] + '>'
            return metadata_str
    
        except:
            return "Failed to get metadata, .params is not created."
                   
    def all_loaded(self) -> bool:
        
        return not (
                   self.acd == None or \
                   self.acr == None or \
                   self.acrv == None or \
                   self.osu == None or \
                   self.osuho == None or \
                   self.osutp == None or \
                   self.params == None or \
                   self.plyrid == None or \
                   self.ppshift == None 
                   )
        
    def parse_osu(self) -> bool:
        
        if (self.all_loaded()):
            print("[SKIP PARSING] " + self.get_beatmap_metadata())
            return True
        try:
            if (self.params['reject'] == True):
                print("[SKIP PARSING <REJECT>] " + self.get_beatmap_metadata())
                return True
        except KeyError:
            pass
        
        if (self.soft_load_flag):
            print("[FORCING HARD LOAD]")
            self.hard_load()

        print("[BEGIN PARSING] " + self.get_beatmap_metadata())
        
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
            print(' -----------')
            print(self.get_beatmap_metadata())
            user_input = ''
            
# =============================================================================
# =============================================================================
# #             # TEMPORARY CODE
# =============================================================================
# =============================================================================
            
            # This automatically accepts any map with less than 75 timing points
            if (len(self.osutp) < 75):
                print("Automatically accepted. TP Len {tplen}"\
                      .format(tplen=len(self.osutp)))
                user_input = 'n'

# =============================================================================
# =============================================================================
# #             # TEMPORARY CODE
# =============================================================================
# =============================================================================           
            
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
            # Make sure to overwrite it by specifying last arg as False
            self.io.save('params', str(self.params), False)
            print("[CREATED] ----------")
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
#            
#   This is also where we correct the 8K Bias, it's a separate mapping compared
#   to the generic 8k model
# =============================================================================

        print("[ACD]", end=' ')
        if (self.acd == None):
            self.acd = osuho_to_acd.run(self.osuho, self.params['keys'], \
                                        self.params['special_style'])
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
            print(' ---------<--------><--------><--------><--------><-------->')
            self.acr = plyrid_to_acr.run(self.plyrid, self.beatmap_id, \
                                         self.params['keys'], self.params['special_style'])
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
            print("[CREATED] ------<--------><--------><--------><--------><-------->")
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

            ppshift_str = '\n'.join(list(map(str, self.ppshift)))

            self.io.save('ppshift', ppshift_str, True)   
            print("[CREATED]")
        else:
            print("[EXISTS]")
            
# =============================================================================
#   End    
# =============================================================================
        print("[END PARSING] " + self.get_beatmap_metadata())
        return True
    
class parse_beatmap_file_name:
    
    def __init__(self, beatmap_file_name: str='', beatmap_id: int=0, soft_load_flag=False):
        
        self.beatmap_id = beatmap_id
        self.beatmap_file_name = beatmap_file_name
        self.soft_load_flag = soft_load_flag
                
        self.io = interface_io.interface_io(beatmap_file_name,\
                                            base_dir = "D:\\Data Documents\\ppshift\\ppshift_ml\\documents\\eval\\")
        
        # Soft load only gets the file's existence
        # This is much faster to check if it's done
        self.soft_load()
        
        # Hard load evaluates the file
        if (not soft_load_flag):
            self.hard_load()
            
        # We will load params anyway, it's not slow
        self.params = self.io.load('params')
        if (self.params):
            self.params = eval(self.params)
        if (self.params == None):
            self.params = {}

    def soft_load(self):
        self.osu = self.io.exist('osu')
        self.osuho = self.io.exist('osuho')
        self.osutp = self.io.exist('osutp')
        self.acd = self.io.exist('acd')
        self.ppshift = self.io.exist('ppshift')

    def hard_load(self):
        self.soft_load_flag=False
        
        self.osu = self.io.load('osu')
        self.osuho = self.io.load('osuho')
        self.osutp = self.io.load('osutp')
        self.acd = self.io.load('acd')
        self.ppshift = self.io.load('ppshift')
        
        if (self.osu):
            self.osu = self.osu.splitlines()
        if (self.osuho):
            self.osuho = list(map(eval, self.osuho.splitlines()))
        if (self.osutp):
            self.osutp = list(map(eval, self.osutp.splitlines()))
        if (self.acd):
            self.acd = list(map(eval, self.acd.splitlines()))
        if (self.ppshift):
            self.ppshift = list(map(eval, self.ppshift.splitlines()))  
     
    def get_beatmap_metadata(self) -> str:
        try:
            metadata_str = \
            self.params['artist'] + ' - ' + \
            self.params['title'] + ' (' + \
            self.params['version'] + ') <' + \
            self.params['creator'] + '>'
            return metadata_str
    
        except:
            return "Failed to get metadata, .params is not created."
                   
    def all_loaded(self) -> bool:
        
        return not (
                   self.acd == None or \
                   self.osu == None or \
                   self.osuho == None or \
                   self.osutp == None or \
                   self.params == None or \
                   self.ppshift == None 
                   )
        
    def parse_osu(self) -> bool:
        
        if (self.all_loaded()):
            print("[SKIP PARSING] " + self.get_beatmap_metadata())
            return True
        try:
            if (self.params['reject'] == True):
                print("[SKIP PARSING <REJECT>] " + self.get_beatmap_metadata())
                return True
        except KeyError:
            pass
        
        if (self.soft_load_flag):
            print("[FORCING HARD LOAD]")
            self.hard_load()

        print("[BEGIN PARSING] " + self.get_beatmap_metadata())
        
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
            self.io.save('params', str(self.params), True)
            print("[CREATED]")
        else:
            print("[EXISTS]")

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
#            
#   This is also where we correct the 8K Bias, it's a separate mapping compared
#   to the generic 8k model
# =============================================================================

        print("[ACD]", end=' ')
        if (self.acd == None):
            self.acd = osuho_to_acd.run(self.osuho, self.params['keys'], \
                                        self.params['special_style'])
            if (self.acd == None):
                raise AssertionError('Fail to convert Hit Objects to Action Difficulty')
            
            acd_str = '\n'.join(list(map(str, self.acd)))
            
            self.io.save('acd', acd_str, True)
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
            self.ppshift = ac_to_ppshift.run(self.acd)
            if (self.ppshift == None):
                raise AssertionError('Fail to convert Actions to PPShift')

            ppshift_str = '\n'.join(list(map(str, self.ppshift)))

            self.io.save('ppshift', ppshift_str, True)   
            print("[CREATED]")
        else:
            print("[EXISTS]")
            