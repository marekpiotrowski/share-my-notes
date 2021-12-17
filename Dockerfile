FROM ubuntu:20.04


RUN apt update

RUN apt -y upgrade

RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update
RUN apt install python3.8 -y
RUN apt install python3.8-venv -y

RUN python3 -m venv /opt/share_my_notes_venv
COPY requirements.txt .

RUN . /opt/share_my_notes_venv/bin/activate && pip install -r requirements.txt
