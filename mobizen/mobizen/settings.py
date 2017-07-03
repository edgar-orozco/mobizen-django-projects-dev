"""
Django settings for mobizen project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import djcelery
djcelery.setup_loader()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5de%dfaws(#7_%6rifo6dt6c_0ad)e2jt+hqgx#7i%@xt%!vzm'

SECURE_HSTS_SECONDS = 0
# 
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'oauth2_provider',
    'corsheaders',
    'social.apps.django_app.default',
    'rest_framework_social_oauth2',
    'rest_framework',
    'djoser',
    'verifica',
    'verifica_news',
    'django_extensions',
    'requests',
    'dateutil',
    'nested_inline',
    'axes',
    'dashboard',
    'bootstrap3',
    'servicios',
    'selectable',
    'drivemee',
    'datetimewidget',
    'django_modalview',
    'bootstrap3_datetime',
)

MIDDLEWARE_CLASSES = (
#     'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
#     'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'mobizen.urls'

WSGI_APPLICATION = 'mobizen.wsgi.application'

SESSION_COOKIE_SECURE = False

CSRF_COOKIE_SECURE = False

CSRF_COOKIE_HTTPONLY = True

X_FRAME_OPTIONS = 'DENY'

SECURE_SSL_REDIRECT = False

SECURE_CONTENT_TYPE_NOSNIFF = False

SECURE_BROWSER_XSS_FILTER = False

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

AXES_LOCK_OUT_AT_FAILURE = False

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '127.0.0.1:11211',
#         'TIMEOUT': 5,
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'postgresql': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ebdb',
        'USER': 'mobizen',
        'PASSWORD': 'mobizen1',
        'HOST': 'aaolof6u3jls2s.cr8nj3k5camn.us-east-1.rds.amazonaws.com',
        'PORT': '5432',
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql', 
#         'NAME': 'django',
#         'USER': 'django',
#         'PASSWORD': 'm0b1z3n',
#         'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
#         'PORT': '3306',
#     }
# }

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'django',
#         'USER': 'django',
#         'PASSWORD': 'SjTsuZmnF2',
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_L10N = True

USE_TZ = True

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'no-reply@mobizen.com.mx'
EMAIL_HOST_PASSWORD = 'mobizenNR201015'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

PHONENUMBER_DEFAULT_REGION = 'mx'
PHONENUMBER_DB_FORMAT = 'NATIONAL'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/home/django/django-projects/mobizen/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/django/django-projects/mobizen/media/'

CORS_ORIGIN_ALLOW_ALL = True

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
}

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    #'PAGINATE_BY': 10,
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
#     'DEFAULT_PERMISSION_CLASSES': [
# #         'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
#         'rest_framework.permissions.DjangoModelPermissions',
#         'rest_framework.permissions.IsAuthenticated'
#         #'rest_framework.authentication.BasicAuthentication',
#         #'rest_framework.authentication.SessionAuthentication',
#     ]
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
#         'rest_framework.authentication.BasicAuthentication',
#         'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
    )
}

DJOSER = {
    'DOMAIN': 'pzmury5.verifica.mx',
    'SITE_NAME': 'Verifica',
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': False,
    'PASSWORD_VALIDATORS': [],
    'SERIALIZERS': {},
}

AUTHENTICATION_BACKENDS = (

    # Others auth providers (e.g. Google, OpenId, etc)

    # Facebook OAuth2
    'social.backends.facebook.FacebookAppOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',

    # django-rest-framework-social-oauth2
    'rest_framework_social_oauth2.backends.DjangoOAuth2',

    # Django
#     'mobizen.backends.UserModelEmailBackend',    # Login w/ email
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_FACEBOOK_KEY = '124756880957995'
SOCIAL_AUTH_FACEBOOK_SECRET = 'b7b8dd9f40a5229a980872b43f8742b6'
# Define SOCIAL_AUTH_FACEBOOK_SCOPE to get extra permissions from facebook. Email is not sent by default, to get it, you must request the email permission:
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '734152608693-59g1t7tiil08dau4oq60rbqacnuic6a0.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'CpZ1AXnI2XtXfkE5f9gzQ04L'
#SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [...]

SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True


BOOTSTRAP3 = {
    'javascript_in_head': True,
    'include_jquery': True,
}
# django-inplaceedit customization


#INPLACEEDIT_EDIT_EMPTY_VALUE = 'Double click to edit...'
# INPLACEEDIT_AUTO_SAVE = True
# INPLACEEDIT_EVENT = 'click'
#INPLACEEDIT_DISABLE_CLICK = False
#INPLACEEDIT_EDIT_MESSAGE_TRANSLATION = 'Write a translation...'
#INPLACEEDIT_SUCCESS_TEXT = 'Successfully saved...'
#INPLACEEDIT_UNSAVED_TEXT = 'You have unsaved changes!!!!'
#INPLACE_ENABLE_CLASS = 'enable'
#DEFAULT_INPLACE_EDIT_OPTIONS = {}
#DEFAULT_INPLACE_EDIT_OPTIONS_ONE_BY_ONE = False
# ADAPTOR_INPLACEEDIT_EDIT = 'inplaceeditform.perms.AdminDjangoPermEditInline'
#ADAPTOR_INPLACEEDIT = {}
#INPLACE_GET_FIELD_URL = None
#INPLACE_SAVE_URL = None
#INPLACE_FIELD_TYPES = 'input, select, textarea'
#INPLACE_FOCUS_WHEN_EDITING = True

# django-inplaceedit-bootstrap customization

# INPLACEEDIT_EDIT_TOOLTIP_TEXT = 'Click to edit' # By default 'Double click to edit'
# ADAPTOR_INPLACEEDIT = {}
# If inplaceeditform_extra_fields is installed
# try:
#     import inplaceeditform_extra_fields
#     INSTALLED_APPS += ('inplaceeditform_extra_fields',)
#     ADAPTOR_INPLACEEDIT = {'image_thumb': 'inplaceeditform_extra_fields.fields.AdaptorImageThumbnailField',
#                            'tiny': 'inplaceeditform_extra_fields.fields.AdaptorTinyMCEField',
#                            'tiny_simple': 'inplaceeditform_extra_fields.fields.AdaptorSimpleTinyMCEField'}
#     try:
#         import sorl
#         INSTALLED_APPS += ('sorl.thumbnail',)
#         THUMBNAIL_DEBUG = DEBUG
#     except ImportError:
#         pass
# except ImportError:
#     pass

# If bootstrap3_datetime is installed
# try:
#     import bootstrap3_datetime
#     ADAPTOR_INPLACEEDIT = ADAPTOR_INPLACEEDIT or {}
#     ADAPTOR_INPLACEEDIT['date'] = 'inplaceeditform_bootstrap.fields.AdaptorDateBootStrapField'
#     ADAPTOR_INPLACEEDIT['datetime'] = 'inplaceeditform_bootstrap.fields.AdaptorDateTimeBootStrapField'
#     ADAPTOR_INPLACEEDIT['datetimepicker'] = 'inplaceeditform_bootstrap.fields.AdaptorDateTimeBootStrapField'
# except ImportError:
#     pass

#BROKER_URL = 'amqp://guest:guest@localhost:5672/'
CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
#CELERYD_CONCURRENCY=2

