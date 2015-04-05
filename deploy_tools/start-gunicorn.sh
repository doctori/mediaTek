#!/bin/bash

NAME="mediaTek"                               # Name of the application
SERVER="dev.lerouge.info"
DJANGODIR=/app             # Django project directory
SOCKFILE=/var/gunicorn/$SERVER  # we will communicate using this unix socket
USER=mediaTek
GROUP=$USER
NUM_WORKERS=4                                     # how many worker processes should Gunicorn spawn
DJANGO_WSGI_MODULE=mediaTek.wsgi                     # WSGI module nameœ
echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR
LOGDIR=/var/log/gunicorn
test -d $LOGDIR || mkdir -p $LOGDIR
chown $USER:$GROUP $LOGDIR
# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec /usr/local/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \

