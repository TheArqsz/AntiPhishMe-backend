import os
import multiprocessing

from config import DEBUG, HOST, PORT, ENVIRONMENT, LOCAL_ENVIRONMENTS, DOCKER_LOCAL_ENVIRONMENTS

bind = f"{HOST}:{PORT}"

backlog = 2048

errorlog = '-'
loglevel = 'debug' if DEBUG else 'info'
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

user = 'gunicorn'

if ENVIRONMENT.lower() in LOCAL_ENVIRONMENTS + DOCKER_LOCAL_ENVIRONMENTS :
    workers = 1
else:
    workers = multiprocessing.cpu_count() * 2 + 1

timeout = 5 * 60  # 5 minutes
keepalive = 24 * 60 * 60  # 1 day