# ec-by-django

## setup
```shell
python manage.py migrate
# run with dev tool
python manage.py runserver
# run with gunicorn(wsgi)
gunicorn app.wsgi --reload
```

## to create stg/prod environment to load env settings file
```shell
export DJANGO_PROFILE=stagging
# or 
export DJANGO_PROFILE=production
```