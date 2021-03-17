FROM continuumio/miniconda3
MAINTAINER aaron_todd

RUN apt-get update
RUN apt-get install -y xvfb
RUN apt-get install -y libgtk2.0-0
RUN apt-get install -y libgconf-2-4
RUN apt-get install -y chromium

RUN conda install -c anaconda psutil

WORKDIR /usr/local/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]

