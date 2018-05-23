FROM python:2.7
ADD . /app
WORKDIR /app
RUN pip install -r requrements.txt
RUN cp config.py.sample config.py
