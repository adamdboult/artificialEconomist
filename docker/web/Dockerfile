FROM node:22

WORKDIR /app

COPY package.json package-lock.json .

RUN npm ci --production

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

