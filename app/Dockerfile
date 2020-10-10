FROM python:3.8

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY p-tracks.py /app
CMD python p-tracks.py