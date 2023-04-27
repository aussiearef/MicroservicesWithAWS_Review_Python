FROM python:3.9
WORKDIR /App

COPY . ./

RUN pip3 install --upgrade pip
RUN pip3 install fastapi
RUN pip3 install boto3

RUN apt update
RUN apt upgrade
RUN apt install -y curl

EXPOSE 80

ENTRYPOINT ['python', 'Review.py']