FROM node:22
RUN npm install -g npm@latest

WORKDIR /app

COPY package.json package-lock.json ./

# Setting NODE_ENV means the development packages get skipped
ENV NODE_ENV=production
RUN npm ci

# Don't want to copy everything because docker for this project is split between this and tensorflow
#COPY . .
#COPY server.js src config Makefile ./
COPY Makefile .
COPY server.js .
COPY src ./src
COPY config ./config

RUN make
#RUN make || (echo "Make failed. Folder layout:" && ls -alR . && exit 1)

CMD [ "node", "server.js", "80", "artificialeconomist-mongo", "27017", "artificialeconomist-tensorflow", "8008" ]

