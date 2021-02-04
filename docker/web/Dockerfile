# Use the official image as a parent image.
FROM node:10

# Update/upgrade
RUN apt-get update && apt-get -y upgrade

# Install basic stuff
RUN apt-get -y install build-essential apache2 git

# Install python
RUN apt-get -y install python3

# Set the working directory.
WORKDIR /usr/src/artificialeconomist

# Copy the file from your host to your current location.
COPY . .

# Install
RUN npm install
RUN npx gulp

# Add metadata to the image to describe which port the container is listening on at runtime.
EXPOSE 8080

# Run the specified command within the container.
CMD [ "node", "server.js", "8080", "artificialeconomist_mongo", "27518" ]

