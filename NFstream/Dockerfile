FROM ubuntu:20.04

RUN apt-get update && apt-get install -y software-properties-common gcc && \
    add-apt-repository -y ppa:deadsnakes/ppa

RUN apt-get update && apt-get install -y python3.6 python3-distutils python3-pip python3-apt

# RUN apt install git

RUN pip3 install numpy

RUN pip3 install pandas

RUN pip3 install sklearn

RUN pip3 install pyspark

RUN pip3 install nfstream

ADD . /NFStream 

