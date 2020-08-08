import os

from werkzeug.serving import run_simple

from config.wsgi import application

PISMA_HOST = os.getenv("PISMA_HOST", "::")
PISMA_PORT = int(os.getenv("PISMA_PORT", "8000"))

if __name__ == "__main__":
    run_simple(PISMA_HOST, PISMA_PORT, application)
