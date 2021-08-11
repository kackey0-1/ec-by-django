import environ

from .base import *

# Read .env if exists
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))


#####################
# Security settings #
#####################
DEBUG = False
SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = ['*']


############
# Database #
############
DATABASES = {
    'default': env.db()
}
DATABASES['default']['ATOMIC_REQUESTS'] = True


###########
# Logging #
###########
LOGGING = {
    # バージョンは「1」固定
    'version': 1,
    # 既存のログ設定を無効化しない
    'disable_existing_loggers': False,
    # ログフォーマット
    'formatters': {
        # 本番用
        'production': {
            'format': '%(asctime)s [%(levelname)s] %(process)d %(thread)d '
                      '%(pathname)s:%(lineno)d %(message)s'
        },
    },
    # ハンドラ
    'handlers': {
        # コンソール出力用ハンドラ
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'production',
        },
    },
    # ロガー
    'loggers': {
        # 自作アプリケーション全般のログを拾うロガー
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # Django本体が出すログ全般を拾うロガー
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        # 発行されるSQL文を出力するための設定
        # 'django.db.backends': {
        #     'handlers': ['console'],
        #     'level': 'DEBUG',
        #     'propagate': False,
        # },
    },
    # # ハンドラ
    # 'handlers': {
    #     # ファイル出力用ハンドラ
    #     'file': {
    #         'level': 'INFO',
    #         'class': 'logging.FileHandler',
    #         'filename': 'app.log'.format(PROJECT_NAME),
    #         'formatter': 'production',
    #     },
    # },
    # # ロガー
    # 'loggers': {
    #     # 自作アプリケーション全般のログを拾うロガー
    #     '': {
    #         'handlers': ['file'],
    #         'level': 'INFO',
    #         'propagate': False,
    #     },
    #     # Django本体が出すログ全般を拾うロガー
    #     'django': {
    #         'handlers': ['file'],
    #         'level': 'INFO',
    #         'propagate': False,
    #     },
    # },
}

##################
# Staticfiles
##################
# STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
AWS_ACCESS_KEY_ID = env.get_value('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env.get_value('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'django-static-resource'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
AWS_DEFAULT_ACL = None
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


##################
# Email settings #
##################
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_CONFIG = env.email_url('EMAIL_URL')
# vars().update(EMAIL_CONFIG)


