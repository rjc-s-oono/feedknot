# -*- coding: utf-8 -*-
# Django settings for feedknot project.
import os

try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = False

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        #'NAME': 'feedknot.db',                      # Or path to database file if using sqlite3.
        'NAME':  os.path.realpath(os.path.join(BASE_DIR, '../../../feedknot.db')), # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Tokyo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ja'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.realpath(os.path.join(BASE_DIR, '../../media'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.realpath(os.path.join(BASE_DIR, '../../static'))

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

#STATIC_MEDIA_DIR = BASE_DIR+os.sep+'..'+os.sep+'..'+os.sep+'media'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'v0#5i(+-pi63z&amp;@)vai^zs^jp=sf05hr-ocd^u20@nv+s9c72#'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

from django.conf import global_settings
TEMPLATE_CONTEXT_PROCESSORS = \
    global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',

    # 追加
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",

    'feedknot.context_processors.staticQueryString',
    'feedknot.context_processors.debugMode',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.middleware.loggingMiddleware'
)

ROOT_URLCONF = 'feedknot.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'feedknot.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.realpath(os.path.join(BASE_DIR, '../../templates'))
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    'common',

    #'sample',
    'feed',
    'box',
    'administration',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # ... include the providers you want to enable:
    'allauth.socialaccount.providers.twitter',
    #'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google'
    #'allauth.socialaccount.providers.linkedin',
    #'allauth.socialaccount.providers.openid',
    #'allauth.socialaccount.providers.persona',
    #'allauth.socialaccount.providers.soundcloud',
    #'allauth.socialaccount.providers.stackexchange',
)

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email', 'publish_stream'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'METHOD': 'oauth2',
        'LOCALE_FUNC': lambda request: 'ja_JP'
    },
    'github': {
        'SCOPE': ['user:follow', 'gist']
    }
}

LOGIN_REDIRECT_URL = '/'
#LOGIN_URL = '/feedknot/login'

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

QUERY_STRING = "201403231620"

LOG_LEVEL = 'INFO'
LOG_DIR_ROOT = os.path.realpath(os.path.join(BASE_DIR, '../../../'))

try:
    from feedknot.local_settings import *
except ImportError:
    pass

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
from datetime import datetime;
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s (%(pathname)s:%(lineno)d %(funcName)s) [%(process)d:%(thread)d] %(message)s'
        },
        'general': {
            'format': '[%(asctime)s] %(levelname)s %(message)s'
        },
        'simple': {
            'format': '[%(levelname)s] %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level': LOG_LEVEL,
            'class': 'django.utils.log.NullHandler',
        },
        'console':{
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'to_file_common': {
            'level': LOG_LEVEL,
            'class': 'logging.FileHandler',
            'filename': LOG_DIR_ROOT+'/log/app/app_'+datetime.now().strftime("%Y%m%d")+'.log',
            'formatter': 'general'
        },
        'to_file_app': {
            'level': LOG_LEVEL,
            'class': 'logging.FileHandler',
            'filename': LOG_DIR_ROOT+'/log/app/app_'+datetime.now().strftime("%Y%m%d")+'.log',
            'formatter': 'verbose'
        },
        'to_file_js': {
            'level': LOG_LEVEL,
            'class': 'logging.FileHandler',
            'filename': LOG_DIR_ROOT+'/log/app/js_'+datetime.now().strftime("%Y%m%d")+'.log',
            'formatter': 'general'
        },
#        'to_file_bat': {
#            'level': LOG_LEVEL,
#            'class': 'logging.FileHandler',
#            'filename': LOG_DIR_ROOT+'/log/bat/'+datetime.now().strftime("%Y%m%d")+'.log',
#            'formatter': 'verbose'
#        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django': {
            'handlers':['null'],
            'propagate': True,
            'level': LOG_LEVEL,
        },
        'django.request': {
            'handlers': ['mail_admins', 'to_file_app'],
            'level': 'ERROR',
            'propagate': True,
        },
#         'django.db.backends': {
#             'handlers': ['console', 'to_file_app'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
        'common_log': {
            'handlers': ['to_file_common'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'application': {
            'handlers': ['console', 'to_file_app'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'js': {
            'handlers': ['console', 'to_file_js'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
#        'batch': {
#            'handlers': ['console', 'to_file_bat'],
#            'level': LOG_LEVEL,
#            'propagate': True,
 #       },
    }
}

if DEBUG:
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    INTERNAL_IPS = ('127.0.0.1',)

    INSTALLED_APPS += (
        'debug_toolbar',
    )

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]

    def custom_show_toolbar(request):
        return True

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TOOLBAR_CALLBACK': 'feedknot.settings.custom_show_toolbar',
        #'EXTRA_SIGNALS': ['myproject.signals.MySignal'],
    }
    DEBUG_TOOLBAR_PATCH_SETTINGS = False
