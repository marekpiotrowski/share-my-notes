FROM ubuntu:20.04


RUN apt update

RUN apt -y upgrade

RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update
RUN apt install python3.8 -y
RUN apt install python3.8-venv -y
RUN apt install wget -y
RUN apt install firefox -y

RUN python3 -m venv /opt/share_my_notes_venv
COPY requirements.txt .

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux32.tar.gz
RUN mkdir /tmp/geckodriver_dir
RUN tar -xzvf geckodriver* -C /tmp/geckodriver_dir
RUN chmod +x /tmp/geckodriver_dir/geckodriver
RUN export PATH=$PATH:/tmp/geckodriver_dir

RUN . /opt/share_my_notes_venv/bin/activate && pip install -r requirements.txt

COPY share_my_notes_app /share_my_notes_app

CMD . /opt/share_my_notes_venv/bin/activate && python -m share_my_notes_app
