FROM python:3.10
LABEL maintainer="qian2tan"
LABEL version="1.0"
LABEL description="winter final project to cosbi"
# ENV PYTHONUNBUFFERED 1
RUN mkdir /rnafold
WORKDIR /rnafold
COPY . /rnafold/
RUN ["pip", "install", "-r", "requirements.txt"]
# Install vim
RUN ["apt-get", "update"]
RUN ["apt-get", "upgrade", "-y"]
RUN ["apt-get", "install", "-y", "vim"]