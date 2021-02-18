
# Docker compose instructions

Rename the correct compose file as docker-compose.yml then:

```bash
sudo docker-compose build --no-cache
sudo docker-compose up --detach
sudo docker exec -it artificialeconomist_tensorflow sh
```

```bash
sudo docker kill $(sudo docker ps -q)
sudo docker rm $(sudo docker ps -a -q)

sudo docker system prune -af
```

Can interact, eg

```bash
sudo docker exec -it artificialeconomist_tensorflow sh
sudo docker exec -it artificialeconomist_nodejs sh
sudo docker exec -it artificialeconomist_mongo sh
```


# Docker instructions (no compose)

Docker-compose on jetson nano (docker-compose version is pre 1.28?) doesn't support GPUs, so do them separately.

First, build the images.

```bash
sudo docker build -t "ae:tensorflow" -f ./docker/tf/Dockerfile_jetson_no_compose.gpu .
#sudo docker build -t "ae:tensorflow" -f ./docker/tf/Dockerfile_jetson.gpu .
sudo docker build -t "ae:web" -f ./docker/web/Dockerfile .
```

```bash
sudo docker run --name artificialeconomist_mongo --detach -v /data/db/artificialeconomist_mongo:/data/db --expose 27017 webhippie/mongodb mongod --port 27017 --bind_ip 0.0.0.0

sudo docker run --name artificialeconomist_tensorflow --gpus all --detach --expose 8008 --link artificialeconomist_mongo:artificialeconomist_mongo ae:tensorflow
sudo docker run --name artificialeconomist_tensorflow --gpus all --detach --expose 8008 -p 8008:8008 --link artificialeconomist_mongo:artificialeconomist_mongo ae:tensorflow

sudo docker run --name artificialeconomist_nodejs --detach --link artificialeconomist_tensorflow:artificialeconomist_tensorflow --link artificialeconomist_mongo:artificialeconomist_mongo -p 8080:80 ae:web
```

Notes below


```bash
sudo docker build -t "nhp:Dockerfile" -f ./docker/tf/Dockerfile_jetson_no_compose.gpu .
sudo docker run --gpus all --detach -p 8008:8008 nhp:Dockerfile
sudo docker run --gpus all -p 8008:8008 nhp:Dockerfile

sudo docker build -t "nhp:Dockerfile" -f ./docker/tf/Dockerfile_jetson_no_compose.cpu .
sudo docker run --gpus all --detach -p 8008:8008 nhp:Dockerfile
sudo docker run --gpus all -p 8008:8008 nhp:Dockerfile


sudo docker ps
sudo docker exec -it <ID> sh

sudo docker exec -it artificialeconomist_tensorflow sh
sudo docker exec -it artificialeconomist_mongo sh
sudo docker exec -it artificialeconomist_nodejs sh


#wget ', ["-qO-", tf_domain + ":" + tf_port + "/" + id_and_question]);
wget localhost:8008/testquestion

wget artificialeconomist_tensorflow:8008/testquestion
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


