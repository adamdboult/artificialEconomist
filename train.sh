cd gpt-2/
sudo PYTHONPATH=src ./train.py --dataset ../merged_file_clean.txt --batch_size 1 --save_every 10000 --sample_every 1000
