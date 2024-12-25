#!/usr/bin/env python3
"""
Hi
"""
##########
# IMPORT #
##########

import shutil
import os
import urllib.request

import string
import re

import requests
from bs4 import BeautifulSoup


bs = BeautifulSoup


######################
# GET FILES TO CLEAN #
######################
print(1)
current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)
source_dir = os.path.join(current_dir, "TXT_raw")
print(source_dir)
source_list = os.listdir(source_dir)
# print(source_list)

dest_dir = os.path.join(current_dir, "TXT_clean")

###############
# CLEAN FILES #
###############
i = 1

printable = set(string.printable)
for source in source_list:
    print("At", i, "of", len(source_list))
    # if i == 1:
    #    continue
    source_path = os.path.join(current_dir, "TXT_raw", source)
    dest_path = os.path.join(current_dir, "TXT_clean", source)
    # print(1)
    # print(source_path)
    # print(source)
    output_rows = []
    with open(source_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            skip = 0

            line = re.sub(r"[^\x00-\x7f]", r"", line)
            line = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]", "", line)
            # line = filter(lambda x: x in printable, line)
            # print(line)

            if len(line) < 15:
                skip = 1
            if skip == 0:
                output_rows.append(line)
            # print(len(line))
            # print(line)
            # print(skip)
        # print(output_rows)
    i = i + 1
    with open(dest_path, "w") as f:
        for row in output_rows:
            f.write(row)
