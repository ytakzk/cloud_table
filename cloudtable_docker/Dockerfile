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
    scipy \
    requests

RUN pip3 install git+https://github.com/daavoo/pyntcloud \
    https://download.pytorch.org/whl/cpu/torch-0.4.1-cp36-cp36m-linux_x86_64.whl

# expose ports
EXPOSE 9997-9999

RUN mkdir /cloud_table

# fetch from github
# WORKDIR /
# RUN git clone git@github.com:ytakzk/cloud_table.git

# # build pointcloud2mesh
# WORKDIR /cloud_table/pointcloud2mesh
# RUN mkdir build
# WORKDIR /cloud_table/pointcloud2mesh/build
# RUN cmake ..
# RUN make

# # fetch point clouds
# WORKDIR /cloud_table/data
# RUN curl -L -o ./04379243.zip https://www.dropbox.com/s/fpzchkh1zwvjkn6/04379243.zip?dl=0
# RUN unzip ./04379243.zip
# RUN rm -f 04379243.zip
# RUN mkdir 04379243_csv

# # convert the format of point clouds to csv
# WORKDIR /cloud_table/table_generator
# RUN python3 convert_ply_to_csv.py

# WORKDIR /cloud_table/python
# RUN python3 webapp.py
