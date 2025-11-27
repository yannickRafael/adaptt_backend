import multiprocessing

# Server socket
bind = "0.0.0.0:5001"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = "/home/ubuntu/adaptt_backend/logs/gunicorn-access.log"
errorlog = "/home/ubuntu/adaptt_backend/logs/gunicorn-error.log"
loglevel = "info"

# Process naming
proc_name = "adaptt_backend"

# Server mechanics
daemon = False
pidfile = "/home/ubuntu/adaptt_backend/gunicorn.pid"
