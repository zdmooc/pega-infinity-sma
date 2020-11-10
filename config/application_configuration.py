import os
from urllib.parse import urlparse


class AppConfig:
    # Django settings
    PISMA_DJANGO_SECRET_KEY = os.getenv("PISMA_DJANGO_SECRET_KEY", "SECRET_KEY")
    PISMA_DJANGO_DEBUG = bool(os.getenv("PISMA_DJANGO_DEBUG", "False") == "True")
    PISMA_DJANGO_SELF_SERVE_STATIC_FILES = bool(
        os.getenv("PISMA_DJANGO_SELF_SERVE_STATIC_FILES", "True") == "True"
    )

    # Loggings ettings
    PISMA_DJANGO_CONSOLE_LOGGING_LEVEL = os.getenv(
        "PISMA_DJANGO_CONSOLE_LOGGING_LEVEL", "WARNING"
    )
    PISMA_DJANGO_FILE_LOGGING_LEVEL = os.getenv(
        "PISMA_DJANGO_FILE_LOGGING_LEVEL", "INFO"
    )
    PISMA_DJANGO_ROOT_LOGGING_LEVEL = os.getenv(
        "PISMA_DJANGO_ROOT_LOGGING_LEVEL", "ERROR"
    )
    PISMA_DJANGO_PISMA_LOGGING_LEVEL = os.getenv(
        "PISMA_DJANGO_PISMA_LOGGING_LEVEL", "INFO"
    )

    # Database settings
    PISMA_DJANGO_SQL_ENGINE = os.getenv(
        "PISMA_DJANGO_SQL_ENGINE", "django.db.backends.sqlite3"
    )
    PISMA_DATABASE_URL = urlparse(os.getenv("PISMA_DATABASE_URL", ""))

    # Pega API settings
    PISMA_PEGAAPI_TIMEOUT = int(os.getenv("PISMA_PEGAAPI_TIMEOUT", "5"))

    # Server settings
    PISMA_HOST = os.getenv("PISMA_HOST", "::")
    PISMA_PORT = int(os.getenv("PISMA_PORT", "8888"))
