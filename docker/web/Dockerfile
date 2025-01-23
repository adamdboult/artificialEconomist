FROM node:22
#RUN apt-get update && apt-get install --no-install-recommends --yes \
#  build-essential                                                   \
#  && apt-get clean                                                  \
#  && rm -rf /var/lib/apt/lists/*                                    \
#  && rm -rf /usr/share/doc/* /usr/share/man/*
#  python3.11-full                                                   \

# Needed for the empty folder stuff to work
WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci

COPY . .

RUN make

CMD [ "node", "server.js", "80", "artificialeconomist-mongo", "27017", "artificialeconomist-tensorflow", "8008" ]

