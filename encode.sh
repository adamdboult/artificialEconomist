#!/usr/bin/env bash
cd ./gpt-2/
#sudo PYTHONPATH=src python ./encode.py ../merged_file_clean_2.txt ../merged_file_clean.txt.npz
sudo PYTHONPATH=src python3 ./encode.py ../getText/merged_file_clean_2.txt ../getText/merged_file_clean.txt.npz
