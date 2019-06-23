# Introduction
This extends the GPT-2 model by training it on economics data.

# Cloning GPT-2
./install.sh

This will clone the GPT-2 model.

Install the requirements
sudo pip3 install -r ./src/requirements.txt

Download the model
python3 ./src/download_model.py 117M

Follow the instructions around tensor flow from the DEVELOPERS.md file.

Install tensorflow 1.12 (with GPU support, if you have a GPU and want everything to run faster)
pip3 install tensorflow==1.12.0
or
pip3 install tensorflow-gpu==1.12.0

# Preparing training data
Scrape PDFs.
./scrape.py

Convert the PDFs to a single text file.
./toText.sh

Encode the text file.
./encode.sh

# Training the model
Train the model
./train.sh

# Querying the model
Query the model.
./query.sh

# Getting the web server to work

Install APT dependencies:
sudo apt install node npm npx build-essential

Install NPM packages:
npm install

Install Bower components:
npx bower install

Prepare public files with gulp:
npx gulp

Run the webserver:
NODE_ENV=production npx forever start ./server.js

