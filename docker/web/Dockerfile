FROM node:22

WORKDIR /app

COPY package.json pnpm-lock.yaml ./
COPY vendor/pnpm-store ./vendor/pnpm-store
COPY vendor/npm ./vendor/npm

RUN npm install -g ./vendor/npm/pnpm_tgz/pnpm-10.33.0.tgz --prefix vendor/npm/pnpm_bin/

RUN ./vendor/npm/pnpm_bin/bin/pnpm install --offline --frozen-lockfile --prod --store-dir vendor/pnpm-store

#COPY . .
#COPY server.js src config Makefile ./
#COPY Makefile .
#COPY server.js .
COPY server.js Makefile .
COPY src ./src
COPY config ./config

RUN make

CMD [ "node", "server.js", "80", "artificialeconomist-mongo", "27017", "artificialeconomist-tensorflow", "8008" ]

