FROM python:3.9.7-alpine

WORKDIR /3155Project
ADD . /3155Project

RUN pip install -r requirement.txt


CMD ["python", "application.py"]