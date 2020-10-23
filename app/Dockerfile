FROM python:3.8

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY p_tracks.py /app
COPY track_ids.txt /app
COPY id_secret.json /app
CMD python p_tracks.py
