# Gunicorn configuration for Django
import multiprocessing
import os

# Server socket
bind = os.getenv("BIND", "0.0.0.0:8000")
backlog = 2048

# Worker processes
workers = int(os.getenv("WEB_CONCURRENCY", multiprocessing.cpu_count() * 2 + 1))
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "-"
errorlog = "-"
loglevel = os.getenv("LOG_LEVEL", "info")
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "infikar"

# Server mechanics
daemon = False
pidfile = "/tmp/gunicorn.pid"
user = None
group = None
tmp_upload_dir = None

# SSL (if needed)
keyfile = None
certfile = None

# Preload app for better performance
preload_app = True

# Worker timeout
graceful_timeout = 30

# Max header line size
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190