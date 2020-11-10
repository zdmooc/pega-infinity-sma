from werkzeug.serving import run_simple

from config import AppConfig
from config.wsgi import application

if __name__ == "__main__":
    run_simple(AppConfig.PISMA_HOST, AppConfig.PISMA_PORT, application)
