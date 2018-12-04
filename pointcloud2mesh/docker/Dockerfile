FROM ubuntu

MAINTAINER Yuta Akizuki <yt@ytakzk.me>


# install required packages (vim & git are not necessary)
RUN apt-get update && apt-get install -y \
    g++ \
    cmake \
    libcgal-dev \
    build-essential \
    vim \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir mount