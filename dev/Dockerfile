FROM python:3.8.10
ENV PYTHONUNBUFFERED 1

WORKDIR /app
RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY . .