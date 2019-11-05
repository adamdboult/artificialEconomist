#!/usr/bin/env python3
##########
# IMPORT #
##########

import requests
from bs4 import BeautifulSoup
import shutil


import os
    
bs = BeautifulSoup

import urllib.request

######################
# GET FILES TO CLEAN #
######################
print(1)
current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)
source_dir = os.path.join(current_dir, "TXT")
print(source_dir)
source_list = os.listdir(source_dir)
#print(source_list)

###############
# CLEAN FILES #
###############
i = 0
for source in source_list:
    if i == 1:
        continue
    source_path = os.path.join(current_dir, "TXT", source)
    print(1)
    print(source_path)
    #print(source)
    with open(source_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            skip = 0
            if len(line) < 15:
                skip = 1
            #print(len(line))
            print(line)
            print(skip)
    i = 1
        

#loop over rows
#remove if blank
#remove if just a number

#remove if length less than 15 characters
