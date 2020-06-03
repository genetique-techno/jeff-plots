FROM continuumio/miniconda3
MAINTAINER aaron_todd

RUN apt-get update
RUN apt-get install -y xvfb
RUN apt-get install -y libgtk2.0-0
RUN apt-get install -y libgconf-2-4
RUN apt-get install -y chromium

RUN conda install -c anaconda psutil
RUN conda install -c plotly plotly-orca

WORKDIR /usr/local/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN mv /opt/conda/bin/orca /opt/conda/bin/orca-exec
RUN echo '#!/bin/bash\nxvfb-run --server-args "-screen 0 1920x1080x24" -a /opt/conda/bin/orca-exec "$@" --disable-gpu' > /opt/conda/bin/orca
RUN chmod +x /opt/conda/bin/orca

CMD ["python", "app.py"]

