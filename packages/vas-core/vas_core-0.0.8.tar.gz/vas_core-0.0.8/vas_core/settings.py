import os, sys
from datetime import timedelta

from dotenv import load_dotenv

from pathlib import Path
PACKAGE_DIR = Path(__file__).resolve().parent

load_dotenv()
AUTH_USER_MODEL = 'app.User'
SECRET_KEY = 'da)(@*#Uhubjindu*(!@#$#@nfoinond-ahp*nen2@=*u)!g8m9pthdg'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


def db(key):
    return os.getenv(key)

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': "django.db.backends.sqlite3",
            'NAME': "test.db"
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': db("PRIMARY_DB_ENGINE"),
            'NAME': db('PRIMARY_DB_NAME'),
            'USER': db('PRIMARY_DB_USER'),
            'PASSWORD': db('PRIMARY_DB_PASSWORD'),
            'HOST': db('PRIMARY_DB_HOST'),
            'PORT': db('PRIMARY_DB_PORT'),
            'CLIENT': {
                'host': db('PRIMARY_DB_HOST')
            }
        },
        'secondary': {
            'ENGINE': db("SECONDARY_DB_ENGINE"),
            'NAME': db('SECONDARY_DB_NAME'),
            'USER': db('SECONDARY_DB_USER'),
            'PASSWORD': db('SECONDARY_DB_PASSWORD'),
            'HOST': db('SECONDARY_DB_HOST'),
            'PORT': db('SECONDARY_DB_PORT'),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(levelname)s] %(asctime)s %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'root': {
        'handlers': ['console', ],
        'level': 'WARNING'
    },
    'loggers': {
        'django.request': {
            'handlers': [
                'console',
            ],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
SAFE_DELETE_FIELD_NAME = "deleted_at"
SAFE_DELETE_CASCADED_FIELD_NAME = "deleted_via_cascade"
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 15,
    'PAGINATE_BY_PARAM': 'limit',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}


REDIS_CONFIG_KEY = "CONFIGURATIONS"

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=30),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=15),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(minutes=30),
}

CORS_ALLOW_ALL_ORIGINS = True
