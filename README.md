
# Setting up GPU on docker

https://nvidia.github.io/nvidia-container-runtime/

Then
https://docs.docker.com/config/containers/resource_constraints/#gpu

# Docker compose instructions

Can't use compose here, see below.

Rename the correct compose file as docker-compose.yml then:

```bash
sudo docker-compose build --no-cache
sudo docker-compose up --detach
```

# Docker instructions (no compose)

Docker-compose on jetson nano (docker-compose version is pre 1.28?) doesn't support GPUs, so do them separately.

First, build the images.

```bash
sudo docker build -t "artificialeconomist-tensorflow" -f ./docker/tf/Dockerfile_jetson.gpu .
sudo docker build -t "artificialeconomist-nodejs" -f ./docker/web/Dockerfile .
```

docker run is docker create and docker start

```bash
sudo docker run --restart=always --detach --name artificialeconomist-mongo -v /data/db/artificialeconomist_mongo:/data/db --expose 27017 mongo:4 mongod --port 27017 --bind_ip 0.0.0.0

sudo docker run --restart=always --detach --name artificialeconomist-tensorflow --gpus all --expose 8008 --link artificialeconomist-mongo:artificialeconomist-mongo ae:tensorflow
sudo docker run --restart=always --detach --name artificialeconomist-tensorflow --expose 8008 --link artificialeconomist-mongo:artificialeconomist-mongo ae:tensorflow

sudo docker run --restart=always --detach --name artificialeconomist-nodejs --link artificialeconomist-tensorflow:artificialeconomist-tensorflow --link artificialeconomist-mongo:artificialeconomist-mongo -p 8080:80 artificialeconomist-nodejs
```


```bash
sudo docker create --restart=always --name artificialeconomist-mongo -v /data/db/artificialeconomist_mongo:/data/db --expose 27017 mongo:4 mongod --port 27017 --bind_ip 0.0.0.0

sudo docker create --restart=always --name artificialeconomist-tensorflow --gpus all --expose 8008 --link artificialeconomist-mongo:artificialeconomist-mongo artificialeconomist-tensorflow
sudo docker create --restart=always --name artificialeconomist-tensorflow --expose 8008 --link artificialeconomist-mongo:artificialeconomist-mongo artificialeconomist-tensorflow

sudo docker create --restart=always --name artificialeconomist-nodejs --link artificialeconomist-tensorflow:artificialeconomist-tensorflow --link artificialeconomist-mongo:artificialeconomist-mongo -p 8080:80 artificialeconomist-nodejs
```


```bash
sudo docker start artificialeconomist-mongo
sudo docker start artificialeconomist-tensorflow
sudo docker start artificialeconomist-nodejs
```


Can check status of containers

```bash
sudo docker ps
sudo docker ps --all
```

Can restart?


```bash
sudo docker start
```

Can test:
```bash
wget artificialeconomist-tensorflow:8008/testquestion
```

# Introduction

This extends the GPT-2 model by training it on economics data.

# Make Jetson Nano headless

temp:
sudo systemctl isolate multi-user.target
persistent
sudo systemctl set-default multi-user.target

OLD:

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


