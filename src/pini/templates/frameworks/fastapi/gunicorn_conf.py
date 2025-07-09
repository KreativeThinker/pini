from config import config

bind = config.gunicorn_bind
workers = config.gunicorn_workers
worker_class = config.gunicorn_worker_class
timeout = config.gunicorn_timeout
