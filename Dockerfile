FROM python:3.9-slim

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

RUN python3 manage.py test

ENTRYPOINT ["/bin/bash", "docker-entrypoint.sh"]
