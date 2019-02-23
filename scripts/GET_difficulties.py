# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
from time import sleep
import random
from datetime import datetime
import os

doc_dir = "D:\\Data Documents\\ppshift\\ppshift_ml\\docs\\"

# ---

def osu_auth():
    
    s = requests.Session()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://osu.ppy.sh/forum/',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers'
            }
    
    auth_file = open('D:\\Data Documents\\auth\\osu.txt', 'r')
    auth_r = auth_file.read().splitlines()
    usr = auth_r[0]
    sec = auth_r[1]
    
    form_data = {
        'username': usr,
        'password': sec,
        'login': 'login'
            }
    
    s.post('https://osu.ppy.sh/', data=form_data, headers=headers)
    
    print(s.cookies)
    
    return s;

# ---
    
def osu_diff_get(beatmap_id: int, session: requests.session):
    
    if (check_diff_exist(beatmap_id)):
        return
    
    r = session.get("https://osu.ppy.sh/osu/" + beatmap_id)
    open(doc_dir + 'difficulties\\' + beatmap_id + '.osu', 'wb+').write(r.content)
    
# ---
    
def osu_beatmap_id_get():
    
    id_file = open(doc_dir + 'regr\\beatmap_ids.csv', 'r')
    id_list = id_file.read().splitlines()
    return id_list

# ---
    
def check_diff_exist(beatmap_id: int):
    
    files = os.listdir(doc_dir + 'difficulties')
    beatmap_id_w_ext = str(beatmap_id) + '.osu'
    return beatmap_id_w_ext in files
    
def main():
    
    session = osu_auth()
    id_list = osu_beatmap_id_get()
    random.seed(datetime.now())
    random.shuffle(id_list)
    id_list = id_list[:3]
    for map_id in id_list:
        sleep(2)
        print("get: " + map_id)
        osu_diff_get(map_id, session)
        
if __name__== "__main__":
    main()

