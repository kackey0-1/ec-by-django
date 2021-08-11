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
    'default': env.db('SQLITE_URL')
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
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    STATIC_URL
]


##################
# Email settings #
##################
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_CONFIG = env.email_url('EMAIL_URL')
# vars().update(EMAIL_CONFIG)


