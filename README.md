
# Docker instructions

```bash
sudo docker-compose build --no-cache
sudo docker-compose up --detach

sudo docker-compose build --file docker-compose_cpu.yml --no-cache
sudo docker-compose up --file docker-compose_cpu.yml --detach

sudo docker-compose build --file docker-compose_gpu.yml --no-cache
sudo docker-compose up --file docker-compose_gpu.yml --detach

```

Can interact, eg
```bash
sudo docker exec -it artificialeconomist_tensorflow sh

sudo docker system prune -a
```

# Introduction

This extends the GPT-2 model by training it on economics data.

# Make Jetson Nano headless

https://devtalk.nvidia.com/default/topic/1049266/jetson-nano/headless-os/
1. Make sure you have a backup
2. Make sure you have ssh enabled (on the card image it is, but make sure...)
3. sudo vi /boot/extlinux/extlinux.conf
4. at the end of the APPEND line, after the rootwait, add 3. The line now looks like:
APPEND ${cbootargs} rootfstype=ext4 root=/dev/mmcblk0p1 rw rootwait 3

# Dependencies

```bash
sudo apt-get install poppler-utils
```

https://docs.nvidia.com/deeplearning/frameworks/install-tf-jetson-platform/index.html

```bash
sudo pip3 install tensorflow-gpu
```

Alternatively, if no GPU,

```bash
pip3 install tensorflow==1.12.0
pip3 install pymongo
```

# Cloning GPT-2

This will clone the GPT-2 model.

```bash
git clone 'https://github.com/nshepperd/gpt-2.git'
sudo pip3 install -r ./gpt-2/requirements.txt
cd gpt-2
python3 ./download_model.py 117M
cd ..
```

If needed, follow the instructions around tensor flow from the DEVELOPERS.md file.

OR NEW

```bash
git clone 'https://github.com/openai/gpt-2'
sudo pip3 install -r ./gpt-2/requirements.txt
cd gpt-2
python3 ./download_model.py 117M
cd ..
```

# Copy server files

```bash
cp new_server.py ./gpt-2/src/
```

# IF SKIP: Copy model

econstormodel/ to ./gpt-2/models/
```bash
econstormodel
```

# SKIP: Preparing training data

Scrape PDFs.

```bash
./scrape.py
```

Also get PDFs from:
https://open.umn.edu/opentextbooks/subjects/economics

Convert the PDFs to a single text file.
```bash
./toText.sh
```

Encode the text file.
```bash
./encode.sh
```

# SKIP: Training the model

Train the model.
```bash
./train.sh
```

# ??Querying the model

Query the model.
```bash
./query.sh
```

# ??Copy the interactive_conditional_samples_AB
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
sudo cp ./node-artificialeconomist.service /lib/systemd/system
sudo cp ./python-artificialeconomist.service /lib/systemd/system
sudo systemctl daemon-reload
sudo systemctl start node-artificialeconomist.service
sudo systemctl start python-artificialeconomist.service
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
sudo cp ./node-artificialeconomist.conf /etc/apache2/sites-available
sudo a2ensite node-artificialeconomist.conf
sudo systemctl reload apache2
```


