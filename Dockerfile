FROM python:3.10 AS base

LABEL maintainer=gavmcmaster@gmail.com
WORKDIR /app

COPY src .
COPY .env .
COPY requirements.txt .
COPY Makefile .

RUN pip install -r requirements.txt

ENV FLASK_APP=stravastats
ENV FLASK_ENV=development

###### Image: Debug ######
FROM base AS debug

RUN pip install debugpy

CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "-m", "flask", "run", "-h", "0.0.0.0", "-p", "5000"]

##### Image: Prod ######
FROM base AS prod

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]