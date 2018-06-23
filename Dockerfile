FROM python:2.7
ADD . /app
WORKDIR /app
RUN pip install -r requrements.txt
