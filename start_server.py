#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)
os.chdir("./gpt-2")
os.system('python3 ./src/new_server.py')
