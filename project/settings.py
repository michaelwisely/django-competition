import os

SETTINGS_DIR = os.path.dirname(__file__)
BUILDOUT_DIR = os.path.dirname(SETTINGS_DIR)
VAR_DIR = os.path.join(BUILDOUT_DIR, "var")

QR_DIR = os.path.join(VAR_DIR, "qr")

# If a secret_settings file isn't defined, open a new one and save a
# SECRET_KEY in it. Then import it.
try:
    from secret_settings import *
except ImportError:
    print "Couldn't find secret_settings file. Creating a new one."
    secret_settings_loc = os.path.join(SETTINGS_DIR, "secret_settings.py")
    with open(secret_settings_loc, 'w') as secret_settings:
        secret_key = ''.join([chr(ord(x) % 90 + 33) for x in os.urandom(40)])
        secret_settings.write("SECRET_KEY = '''%s'''\n" % secret_key)
    from secret_settings import *

# Competition Settings
COMPETITION_DEFAULT_IMAGE = "/static/img/default_competition_image.png"
COMPETITION_DEFAULT_THUMB = "/static/img/default_competition_image_t.png"


# Testing settings
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['--cover-package=competition',  # Only check the
                                             # competition package
                                             # when computing testing
                                             # code coverage

             '--verbosity=2',                # Slightly more verbose
                                             # output

             '--with-yanc',                  # Use colorized output

             # Achievements have been misbehaving. Leave them out for now
             # '--with-achievements',          # Track achievements!
             ]

# Django Debug Toolbar settings
INTERNAL_IPS = ('127.0.0.1',)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

# Crispy setting
CRISPY_TEMPLATE_PACK = 'bootstrap'

# Django Guardian settings
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # this is default
    'guardian.backends.ObjectPermissionBackend',
)
ANONYMOUS_USER_ID = -1

LOGIN_REDIRECT_URL = '/competition/'

ADMINS = (
    # empty
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(VAR_DIR, "db", "competition.db"),
    }
}

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True
USE_L10N = True

MEDIA_ROOT = os.path.join(VAR_DIR, "uploads")
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(VAR_DIR, "static")
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
    os.path.join(SETTINGS_DIR, "static"),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'project.urls'

TEMPLATE_DIRS = (
    os.path.join(SETTINGS_DIR, "templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'debug_toolbar',
    'django_extensions',
    'django_nose',
    'guardian',
    'crispy_forms',
    'competition',

    'south',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
