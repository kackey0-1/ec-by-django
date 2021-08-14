FROM python:3

USER ec-service

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

RUN python3 manage.py test --settings app.settings.test

ENTRYPOINT ["/bin/bash", "docker-entrypoint.sh"]
