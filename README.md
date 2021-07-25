# ec-by-django

## setup
```shell
python manage.py migrate
# run with dev tool
python manage.py runserver
# run with gunicorn(wsgi)
gunicorn app.wsgi --reload
```