FROM node:10
RUN apt-get update && apt-get -y install build-essential apache2 git python3
COPY . .
RUN npm install && npx gulp
CMD [ "node", "server.js", "80", "artificialeconomist_mongo", "27017", "artificialeconomist_tensorflow", "8008" ]
