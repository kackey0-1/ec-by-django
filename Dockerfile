FROM python:3

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

RUN python3 manage.py test --settings app.settings.test

RUN export DJANGO_PROFILE=production

ENTRYPOINT ["/bin/bash", "docker-entrypoint.sh"]
