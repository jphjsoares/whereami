FROM python:3.9

WORKDIR /code

#prevents python from writing .pyc to disk
ENV PYTHONDONTWRITEBYTECODE 1

#prevents python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
