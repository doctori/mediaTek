echo "starting django but waiting 15 sec in order to wait for the DB"
sleep 15;
python3.2 manage.py migrate --noinput
python3.2 manage.py runserver 0.0.0.0:8000
