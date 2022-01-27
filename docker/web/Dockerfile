FROM node:16
RUN apt-get update && apt-get -y install build-essential apache2 git python3 ruby-sass

# Needed for the empty folder stuff to work
WORKDIR /Projects/artificialeconomist/

COPY . .
RUN npm install && make
CMD [ "node", "server.js", "80", "artificialeconomist-mongo", "27017", "artificialeconomist-tensorflow", "8008" ]
