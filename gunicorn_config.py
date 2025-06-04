# gunicorn_config.py
bind = "0.0.0.0:10000"
timeout = 1200  
workers = 1
worker_class = 'sync'
keepalive = 5
max_requests = 100
max_requests_jitter = 10
graceful_timeout = 120