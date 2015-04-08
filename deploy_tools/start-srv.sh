echo "starting django but waiting 15 sec in order to wait for the DB"
sleep 15;
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput
 supervisord -c /etc/supervisor/supervisord.conf -n
