"""These settings are used by the simple-django Buildout part.

Since simple-django installs WAY fewer eggs, this settings file is
much more restricted than settings.py.
"""
import project.development
from project.development import *

# Need DEBUG to be true, otherwise the tests won't run
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Mostly the same as settings.py, but we aren't installing yanc or
# nose-achievements
NOSE_ARGS = ['--cover-package=competition',  # Only check the
                                             # competition package
                                             # when computing testing
                                             # code coverage

             '--verbosity=2',                # Slightly more verbose
                                             # output
             ]

# Same as in settings.py, but only include django's builtin
# middleware. In particular, this should remove django_toolbar's
# middleware. 
dev_middleware = project.development.MIDDLEWARE_CLASSES
MIDDLEWARE_CLASSES = tuple(m for m in dev_middleware if m.startswith('django.'))

# We're not installing anything other than default Django stuff,
# django-guardian, and the competition app
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',

    'guardian',
    'competition',
)

# Using a simplified urlconf since project.urls has URLs that point to
# admin_tools and stuff.
ROOT_URLCONF = 'project.simple_urls'
