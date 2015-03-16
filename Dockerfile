FROM python:3.4
WORKDIR /code
ADD . /code
RUN pip install -r requirements.txt
