echo "starting django but waiting 15 sec in order to wait for the DB"
sleep 15;
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput
python3 manage.py rebuild_index --noinput
chmod 777
 supervisord -c /etc/supervisor/supervisord.conf -n
