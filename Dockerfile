FROM nginx
 WORKDIR /app
 RUN apt-get update
 RUN apt-get install -y python3.2
 RUN apt-get install -y python3-pip python-psycopg2 libpq-dev
 RUN apt-get clean all
 ADD requirements.txt /app/
 RUN pip-3.2 install -r requirements.txt
 ADD deploy_tools/start-srv.sh /src/
