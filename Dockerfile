FROM python:3.9

WORKDIR /3155Project
COPY . .

RUN pip install -r requirement.txt

CMD ["python","application.py"]