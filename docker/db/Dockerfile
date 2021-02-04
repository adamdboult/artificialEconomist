# Use the official image as a parent image.
#FROM mongo:3.6
# Above doesn't work on RPi, so default to Ubuntu.
FROM ubuntu:20.04

# Update/upgrade
RUN apt-get update && apt-get -y upgrade

# Install python
RUN apt-get -y install mongodb

