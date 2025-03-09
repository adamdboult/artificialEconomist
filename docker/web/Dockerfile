FROM node:22

# Needed for the empty folder stuff to work
WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci

COPY . .

RUN make

CMD [ "node", "server.js", "80", "artificialeconomist-mongo", "27017", "artificialeconomist-tensorflow", "8008" ]

