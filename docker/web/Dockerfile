FROM node:22
RUN apt-get update && apt-get -y install \
  build-essential                        \
  python3-full

# Needed for the empty folder stuff to work
WORKDIR /Projects/artificialeconomist/

# Copy package.json and package-lock.json to leverage Docker cache
COPY package.json package-lock.json ./
# Install dependencies using npm ci
RUN npm ci

COPY . .

RUN make

CMD [ "node", "server.js", "80", "artificialeconomist-mongo", "27017", "artificialeconomist-tensorflow", "8008" ]
