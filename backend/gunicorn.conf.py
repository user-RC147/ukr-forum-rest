import os

bind = "0.0.0.0:8080"
workers = os.getenv("GUNICORN_WORKERS", 3)  # (2 × core_amount_cpu) + 1
worker_class = "sync"
timeout = 30
graceful_timeout = 30
keepalive = 5


accesslog = "-"
errorlog = "-"
loglevel = "info"

preload_app = False
