import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("PISMA_DJANGO_SECRET_KEY", "SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.getenv("PISMA_DJANGO_DEBUG", "False") == "True")

ALLOWED_HOSTS = ["*"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "pisma_full": {
            "format": "[{asctime}] [{name}] [{process:d}] [{thread:d}] [{levelname}] [{user}] - {message}",
            "style": "{",
        },
        "common_full": {
            "format": "[{asctime}] [{name}] [{process:d}] [{thread:d}] [{levelname}] - {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": os.getenv("PISMA_DJANGO_CONSOLE_LOGGING_LEVEL", "WARNING"),
            "class": "logging.StreamHandler",
            "formatter": "common_full",
        },
        "pisma_log_file": {
            "level": os.getenv("PISMA_DJANGO_FILE_LOGGING_LEVEL", "INFO"),
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "pisma.log"),
            "formatter": "pisma_full",
        },
        "error_log_file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "errors.log"),
            "formatter": "common_full",
        },
    },
    "root": {
        "handlers": ["console", "error_log_file"],
        "level": os.getenv("PISMA_DJANGO_ROOT_LOGGING_LEVEL", "ERROR"),
    },
    "loggers": {
        "pisma": {
            "handlers": ["console", "pisma_log_file"],
            "level": os.getenv("PISMA_DJANGO_PISMA_LOGGING_LEVEL", "INFO"),
        }
    },
}

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "pisma.apps.PismaConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

LOGIN_URL = "/login/"
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
