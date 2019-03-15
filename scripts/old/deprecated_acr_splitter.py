# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 17:13:36 2019

@author: user
"""

import interface_io
import os


file_l = [x.split('.')[0] for x in os.listdir("D:\\Data Documents\\ppshift\\ppshift_ml\\docs\\difficulties\\conversions\\acr")]
file_l = list(map(int, file_l))

for file in file_l:
    io = interface_io.interface_io(file)
    replay_list = io.load('acr')
    counter = 1
    for replay in replay_list:
        replay_l = eval(replay)
        io.save_nested('acr', str(io.beatmap_id), str(counter), str(replay_l), True)
        counter += 1
