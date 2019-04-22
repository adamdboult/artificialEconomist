
###########
# INSTALL #
###########
sudo apt-get install poppler-utils



#pip3 install regex --ignore-installed
#pip3 install tensorflow --ignore-installed
#pip3 install tensorflow-gpu --ignore-installed
#pip3 install numpy --ignore-installed
#pip3 install tqdm --ignore-installed

#########
# CLONE #
#########
echo "Cloning..."
git clone 'https://github.com/nshepperd/gpt-2.git'

sudo pip3 install -r ./gpt-2/requirements.txt

##################
# DOWNLOAD MODEL #
##################
echo "Downloading model..."
cd gpt-2

python download_model.py 117M

#source activate MY_TENSORFLOW_ENVIRONMENT
