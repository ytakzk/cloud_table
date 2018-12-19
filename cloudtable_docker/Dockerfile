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
    curl \
    unzip \
    python3-minimal \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# install required python packages
RUN pip3 install \
    flask \
    pandas \
    numpy \
    numba \
    scipy

RUN pip3 install git+https://github.com/daavoo/pyntcloud \
    https://download.pytorch.org/whl/cpu/torch-0.4.1-cp36-cp36m-linux_x86_64.whl

RUN mkdir mount

EXPOSE 9997-9999