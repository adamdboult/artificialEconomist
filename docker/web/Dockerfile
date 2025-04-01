FROM node:22
RUN npm install -g npm@latest

WORKDIR /app

COPY package.json package-lock.json ./

ENV NODE_ENV=production
RUN npm ci

#COPY . .
#COPY server.js src config Makefile ./
#COPY Makefile .
#COPY server.js .
COPY server.js Makefile .
COPY src ./src
COPY config ./config

RUN make

CMD [ "node", "server.js", "80", "artificialeconomist-mongo", "27017", "artificialeconomist-tensorflow", "8008" ]

