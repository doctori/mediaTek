echo "starting django but waiting 15 sec in order to wait for the DB"
sleep 15;
python3.2 manage.py migrate --noinput
 supervisord -c /etc/supervisor/supervisord.conf -n
