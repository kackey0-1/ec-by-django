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

## Test
```shell
python manage.py test
# coverage
coverage run --source='.' manage.py test
coverage report
```

## Github actions

1. [Introduction to Github Actions](https://docs.github.com/en/actions/learn-github-actions/introduction-to-github-actions)
2. [Add new encrypted secrets](https://docs.github.com/en/actions/reference/encrypted-secrets)

## Terraform

```bash
terraform destroy -target=module.vpc
```