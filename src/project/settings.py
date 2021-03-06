# Django settings for 'project' project.
import datetime
import os.path
import re

import dotenv

##############################################################################
# Environment overrides
# ---------------------
# Pull in hidden config values using environment variables
HERE = os.path.abspath(os.path.join(os.path.dirname(__file__)))

dotenv.read_dotenv(os.path.join(HERE, '..', '.env'))
env = os.environ

if 'DEBUG' in env:
    DEBUG = TEMPLATE_DEBUG = (env.get('DEBUG').lower() in
                              ('true', 'on', 't', 'yes'))
else:
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG

ADMINS = (
    (env.get('ADMIN_NAME', 'Your Name'),
     env.get('ADMIN_EMAIL', 'your_email@example.com'))
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy',
    }
}

ALLOWED_HOSTS = ['*']

REST_FRAMEWORK = {
    'PAGINATE_BY': 100,
    'PAGINATE_BY_PARAM': 'page_size'
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = os.environ.get('TIME_ZONE', 'America/New_York')

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

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
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'pbv(g=%7$$4rzvl88e24etn57-%n0uw-@y*=7ak422_3!zrc9+'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.auth.context_processors.auth",

    "project.context_processors.settings_context",
)

MIDDLEWARE_CLASSES = (
    'base.middleware.CacheRequestBody',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'project.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'project.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or
    # "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
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

    # 3rd-party reusaple apps
    'jstemplate',
    'compressor',
    'django_extensions',

    # Project apps
    'base',
    'proxy',
)

# Use a test runner that does not use a database.
TEST_RUNNER = 'base.test_runner.DatabaselessTestSuiteRunner'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'base': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

##############################################################################
# Database and storages

if 'DATABASE_URL' in env:
    import dj_database_url
    # NOTE: Be sure that your DATABASE_URL has the 'postgis://' scheme.
    DATABASES = {'default': dj_database_url.config()}
    DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_NAME = 'sa-web-session'

ATTACHMENT_STORAGE = 'django.core.files.storage.FileSystemStorage'
# How long to keep api cache values. Since the api will invalidate the cache
# automatically when appropriate, this can (and should) be set to something
# large.
API_CACHE_TIMEOUT = 3600  # an hour

if 'REDIS_URL' in env or 'REDISCLOUD_URL' in env:
    redis_url = env.get('REDIS_URL') or env.get('REDISCLOUD_URL')
    scheme, connstring = redis_url.split('://')
    if '@' in connstring:
        userpass, netloc = connstring.split('@')
        userename, password = userpass.split(':')
    else:
        userpass = None
        netloc = connstring
    CACHES = {
        "default": {
            "BACKEND": "redis_cache.cache.RedisCache",
            "LOCATION": "%s:0" % (netloc,),
            "OPTIONS": {
                "CLIENT_CLASS": "redis_cache.client.DefaultClient",
                "PASSWORD": password,
            } if userpass else {}
        }
    }
    # Django sessions
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    # Celery broker
    BROKER_URL = redis_url.strip('/') + '/1'

if all([key in env for key in ('SHAREABOUTS_AWS_KEY',
                               'SHAREABOUTS_AWS_SECRET',
                               'SHAREABOUTS_AWS_BUCKET')]):
    AWS_ACCESS_KEY_ID = env['SHAREABOUTS_AWS_KEY']
    AWS_SECRET_ACCESS_KEY = env['SHAREABOUTS_AWS_SECRET']
    AWS_STORAGE_BUCKET_NAME = env['SHAREABOUTS_AWS_BUCKET']
    AWS_QUERYSTRING_AUTH = False
    AWS_PRELOAD_METADATA = True

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    ATTACHMENT_STORAGE = DEFAULT_FILE_STORAGE
    STATICFILES_STORAGE = DEFAULT_FILE_STORAGE
    STATIC_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME


##############################################################################
# Flavor-specific settings

# The SHAREABOUTS['FLAVOR'] environment variable is used as a prefix for the
# Shareabouts configuration. configuration is expected to live in a package
# named 'flavors.<SHAREABOUTS_FLAVOR>'. This package will correspond to a
# folder in the root of the src tree that contains all the configuration
# information for the flavor.
SHAREABOUTS = {
    'FLAVOR': os.environ.get('FLAVOR', 'duwamish_flavor'),
    'DATASET_ROOT': os.environ.get('SITE_URL', 'NO_SITE_URL'),
    'DATASET_KEY': os.environ.get('SITE_KEY', 'NO_SITE_KEY')
}

# TODO: Remove this as it's not needed/used:
if 'SHAREABOUTS_FLAVOR' in env:
    SHAREABOUTS['FLAVOR'] = env.get('SHAREABOUTS_FLAVOR')
if 'SHAREABOUTS_DATASET_ROOT' in env:
    SHAREABOUTS['DATASET_ROOT'] = env.get('SHAREABOUTS_DATASET_ROOT')
if 'SHAREABOUTS_DATASET_KEY' in env:
    SHAREABOUTS['DATASET_KEY'] = env.get('SHAREABOUTS_DATASET_KEY')

# Using print function for logging because handlers are not set in settings.py
if 'FLAVOR' not in os.environ:
    print("INFO: Using default flavor")
if 'SITE_URL' not in os.environ:
    print("ERROR: No SITE_URL found!")
if 'SITE_KEY' not in os.environ:
    print("ERROR: No SITE_KEY found!")

# programatically add environment variables of type *_SITE_URL and
# *_DATASET_KEY
for k in os.environ:
    if re.match('.+_DATASET_KEY$|.+_SITE_URL$', k):
        SHAREABOUTS[k] = os.environ.get(k, 'Error')

# ---------------
# By default, the flavor is assumed to be a local python package.  If no
# CONFIG_FILE or PACKAGE is specified, they are constructed as below.

try:
    # SHAREABOUTS
    flavor = SHAREABOUTS['FLAVOR']
except (NameError, TypeError, KeyError):
    from django.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured('No SHAREABOUTS configuration defined. '
                               'Did you forget to copy the local settings '
                               'template?')

if 'CONFIG' not in SHAREABOUTS:
    SHAREABOUTS['CONFIG'] = os.path.abspath(os.path.join(HERE, '..',
                                                         'flavors', flavor))
if 'PACKAGE' not in SHAREABOUTS:
    SHAREABOUTS['PACKAGE'] = '.'.join(['flavors', flavor])
    INSTALLED_APPS = (SHAREABOUTS['PACKAGE'],) + INSTALLED_APPS

##############################################################################
# Auth settings

if 'SHAREABOUTS_TWITTER_KEY' in env \
   and 'SHAREABOUTS_TWITTER_SECRET' in env:
    SOCIAL_AUTH_TWITTER_KEY = env['SHAREABOUTS_TWITTER_KEY']
    SOCIAL_AUTH_TWITTER_SECRET = env['SHAREABOUTS_TWITTER_SECRET']

if 'SHAREABOUTS_FACEBOOK_KEY' in env \
   and 'SHAREABOUTS_FACEBOOK_SECRET' in env:
    SOCIAL_AUTH_FACEBOOK_KEY = env['SHAREABOUTS_FACEBOOK_KEY']
    SOCIAL_AUTH_FACEBOOK_SECRET = env['SHAREABOUTS_FACEBOOK_SECRET']

##############################################################################
# sitemaps and client-side caching

# For sitemaps and caching -- will be a new value every time the server starts
LAST_DEPLOY_DATE = datetime.datetime.now().replace(second=0,
                                                   microsecond=0).isoformat()

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
from os.path import dirname, abspath, join as pathjoin
STATIC_ROOT = abspath(pathjoin(dirname(__file__), '..', '..', 'staticfiles'))
if (DEBUG):
    COMPRESS_ROOT = abspath(pathjoin(dirname(__file__),
                                     '..',
                                     'base',
                                     'static'))
else:
    COMPRESS_ROOT = STATIC_ROOT
COMPRESS_OUTPUT_DIR = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'
COMPRESS_URL = STATIC_URL

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)
# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    str(os.path.abspath(os.path.join(HERE,
                                     '..',
                                     'flavors',
                                     flavor + "/static"))),
)

##############################################################################
# analytics

if 'GOOGLE_ANALYTICS_ID' in env:
    GOOGLE_ANALYTICS_ID = env.get('GOOGLE_ANALYTICS_ID')
if 'GOOGLE_ANALYTICS_DOMAIN' in env:
    GOOGLE_ANALYTICS_DOMAIN = env.get('GOOGLE_ANALYTICS_DOMAIN')
if 'CLICKY_ANALYTICS_ID' in env:
    CLICKY_ANALYTICS_ID = env.get('CLICKY_ANALYTICS_ID')

##############################################################################
# Services

if 'DEBUG' in env:
    DEBUG = TEMPLATE_DEBUG = (env.get('DEBUG').lower() in
                              ('true', 'on', 't', 'yes'))
# email notification service:
if all(k in env for k in ['EMAIL_ADDRESS', 'EMAIL_HOST', 'EMAIL_PORT',
                          'EMAIL_USERNAME', 'EMAIL_PASSWORD', 'EMAIL_USE_TLS',
                          'EMAIL_NOTIFICATIONS_BCC']):
    EMAIL_ADDRESS = env['EMAIL_ADDRESS']
    EMAIL_HOST = env['EMAIL_HOST']
    EMAIL_PORT = env['EMAIL_PORT']
    EMAIL_HOST_USER = env['EMAIL_USERNAME']
    EMAIL_HOST_PASSWORD = env['EMAIL_PASSWORD']
    EMAIL_USE_TLS = env['EMAIL_USE_TLS']
    EMAIL_NOTIFICATIONS_BCC = env['EMAIL_NOTIFICATIONS_BCC'].split(',')
    EMAIL_DEBUG = (env.get('EMAIL_DEBUG').lower() in
                   ('true', 'on', 't', 'yes'))
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' \
                    if not EMAIL_DEBUG else \
                    'django.core.mail.backends.console.EmailBackend'

# geolocation services:
MAPQUEST_KEY = env.get('MAPQUEST_KEY', 'Fmjtd%7Cluur2g0bnl%2C25%3Do5-9at29u')
MAPBOX_TOKEN = env.get('MAPBOX_TOKEN', '')


##############################################################################
# Locale paths
# ------------
# Help Django find any translation files.

LOCALE_PATHS = (
    os.path.join(HERE, '..', 'base', 'locale'),
    os.path.join(HERE, '..', 'flavors', flavor, 'locale'),
)

if SHAREABOUTS['DATASET_ROOT'].startswith('/'):
    INSTALLED_APPS += (
        # =================================
        # 3rd-party reusaple apps
        # =================================
        'rest_framework',
        'django_nose',
        'storages',
        'social.apps.django_app.default',
        'raven.contrib.django.raven_compat',
        'django_ace',
        'django_object_actions',
        'djcelery',

        # OAuth
        'provider',
        'provider.oauth2',
        'corsheaders',

        # =================================
        # Project apps
        # =================================
        'sa_api_v2',
        'sa_api_v2.apikey',
        'sa_api_v2.cors',
        'remote_client_user',
    )

    ###########################################################################
    # Authentication
    ###########################################################################

    AUTHENTICATION_BACKENDS = (
        # See:
        # http://django-social-auth.readthedocs.org/en/latest/configuration.html
        # for list of available backends.
        'social.backends.twitter.TwitterOAuth',
        'social.backends.facebook.FacebookOAuth2',
        'sa_api_v2.auth_backends.CachedModelBackend',
    )

    AUTH_USER_MODEL = 'sa_api_v2.User'
    SOCIAL_AUTH_USER_MODEL = 'sa_api_v2.User'
    SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email', ]

    SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = ['name', 'picture', 'bio']
    SOCIAL_AUTH_TWITTER_EXTRA_DATA = ['name',
                                      'description',
                                      'profile_image_url']

    # Explicitly request the following extra things from facebook
    SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
        'fields': 'id,name,picture.width(96).height(96),first_name,last_name,bio'
    }

    SOCIAL_AUTH_LOGIN_ERROR_URL = 'remote-social-login-error'

    ############################################################################
    # Background task processing
    ############################################################################

    CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
