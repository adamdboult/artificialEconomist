#!/usr/bin/env bash
cd ./gpt-2/ || exit 1
sudo PYTHONPATH=src ./train.py --dataset ../merged_file_clean.txt.npz --batch_size 1 --save_every 100 --sample_every 100
