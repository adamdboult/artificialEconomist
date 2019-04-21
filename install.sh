#########
# CLONE #
#########
echo "Cloning..."
git clone 'https://github.com/nshepperd/gpt-2.git'

##################
# DOWNLOAD MODEL #
##################
echo "Downloading model..."
cd gpt-2

python download_model.py 117M

#source activate MY_TENSORFLOW_ENVIRONMENT
