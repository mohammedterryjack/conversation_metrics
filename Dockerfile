FROM git.oxolo.com:5050/development/docker/ubuntu20.04/cuda11.0-py38:v1.0.0

WORKDIR /home

ADD requirements.txt .

RUN pip3 install --upgrade pip &&\
    pip install --upgrade pip setuptools &&\
    pip install --default-timeout=1000 -r requirements.txt

ADD . /home