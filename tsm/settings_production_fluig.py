import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = 'iczggaeda^c-kf!t4e0gotd8i^ts0a+_sy=_s7r$^ucu&o3yuv'

DEBUG = False
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '10.10.2.132', 'tsm.totvs.com.br', '187.94.58.26']

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap_toolkit',
    'django_bootstrap_breadcrumbs',
    'south',
    'tsm.core',
    'tsm.acesso',
    'tsm.cliente',
    'tsm.equipe',
    'tsm.oportunidade',
    'tsm.relatorio',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',

    'tsm.acesso.middleware.PasswordChangeMiddleware',
)

ROOT_URLCONF = 'tsm.urls'
WSGI_APPLICATION = 'tsm.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tsmdb_fluig',                     
        'USER': 'tsmdb_user',
        'PASSWORD': 'G85dXJO1Q72101G',
        'HOST': 'localhost',
        'PORT': '3306',                     
        'HOST': '/var/lib/mysql/mysql.sock',
    }
}
SOUTH_TESTS_MIGRATE = False
LANGUAGE_CODE = 'pt-BR'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
LANGUAGES =(
    ('pt_BR',u'Brasil'),
)

LOCALE_PATHS =(
    os.path.join(BASE_DIR+'/acesso/','/locale'),
)

#Especificacoes para passwords
PASSWORD_MIN_LENGTH = 6
PASSWORD_MAX_LENGTH = 120
PASSWORD_COMPLEXITY = {
    "UPPER": 1,       
    "LOWER": 1,       
    "DIGITS": 1,      
    "PUNCTUATION": 1, 
    "NON ASCII": 0,   
    "WORDS": 1        
}

USE_L10N = True
USE_TZ = True

STATIC_ROOT = '/var/www/tsmproducao/'
STATIC_URL = '/static/'

STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        # Include the default Django email handler for errors
        # This is what you'd get without configuring logging at all.
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
             # But the emails are plain text by default - HTML is nicer
            'include_html': True,
        },
        # Log to a text file that can be rotated by logrotate
        'logfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': '/var/log/django/tsm_fluig.log'
        },
    },
    'loggers': {
        # Again, default Django configuration to email unhandled exceptions
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        # Might as well log any errors anywhere else in Django
        'django': {
            'handlers': ['logfile'],
            'level': 'ERROR',
            'propagate': False,
        },
        # Your own app - this assumes all your logger names start with "myapp."
        'myapp': {
            'handlers': ['logfile'],
            'level': 'WARNING', # Or maybe INFO or DEBUG
            'propagate': False
        },
    },
}

#SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2               # Age of cookie, in seconds (default: 2 weeks).
SESSION_COOKIE_AGE = 60 * 60                             # Idade da sessao em segundos, atualmente 1h, significa que 1h sem atividade o sistema desloga o usuario