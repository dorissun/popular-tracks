FROM python:3.8

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY scripts/main.py track_ids.txt id_secret.json ./
COPY popular_tracks popular_tracks/
CMD python main.py
