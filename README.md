# Introduction
This extends the GPT-2 model by training it on economics data.

# Cloning GPT-2
This will clone the GPT-2 model.
```bash
./install.sh
```



Install the requirements
```bash
sudo pip3 install -r ./src/requirements.txt
```

Download the model
```bash
python3 ./src/download_model.py 117M
```

Follow the instructions around tensor flow from the DEVELOPERS.md file.

Install tensorflow 1.12 (with GPU support, if you have a GPU and want everything to run faster)
```bash
pip3 install tensorflow==1.12.0
```
or
```bash
pip3 install tensorflow-gpu==1.12.0
```

# Preparing training data
Scrape PDFs.
```bash
./scrape.py
```

Convert the PDFs to a single text file.
```bash
./toText.sh
```

Encode the text file.
```bash
./encode.sh
```

# Training the model
Train the model
```bash
./train.sh
```

# Querying the model
Query the model.
```bash
./query.sh
```

# Copy the interactive_conditional_samples_AB
 Note that this updates the default top_k and top_p from 0 and 0 respectively.

# Getting the web server to work
Install APT dependencies:
```bash
sudo apt install nodejs npm build-essential
```

Install npx
```bash
sudo npm -g install npx
```

Install NPM packages
```bash
npm install
```

Install Bower components
```bash
npx bower install
```

Prepare public files with gulp
```bash
npx gulp
```

For testing
```bash
node server.js
```

Copy the service file.
```bash
sudo cp node-artificialeconomist.service /lib/systemd/system
sudo systemctl daemon-reload
sudo systemctl start node-artificialeconomist.service
```

# Settings for proxy server

Get certificates for www.artificialeconomist.com and artificialeconomist.com.
```bash
sudo systemctl stop apache2.service
sudo apt install certbot
sudo certbot certbot only
sudo systemctl start apache2.service
```

Forward from proxy server.
```bash
sudo a2enmod rewrite
sudo a2enmod ssl
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo cp node-artificialeconomist.conf /etc/apache2/sites-available
sudo a2ensite node-artificialeconomist.conf
sudo systemctl reload apache2
```

