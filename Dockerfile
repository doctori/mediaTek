FROM nginx
 WORKDIR /app
 RUN apt-get update
 RUN apt-get -y install curl make gcc libssl-dev
 # Install python 3.4
ENV LANG C.UTF-8

ENV PYTHON_VERSION 3.4.3

# gpg: key F73C700D: public key "Larry Hastings <larry@hastings.org>" imported
RUN gpg --keyserver pool.sks-keyservers.net --recv-keys 97FC712E4C024BBEA48A61ED3A5CA953F73C700D

RUN set -x \
	&& mkdir -p /usr/src/python \
	&& curl -SL "https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tar.xz" -o python.tar.xz \
	&& curl -SL "https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tar.xz.asc" -o python.tar.xz.asc \
	&& gpg --verify python.tar.xz.asc \
	&& tar -xJC /usr/src/python --strip-components=1 -f python.tar.xz \
	&& rm python.tar.xz* \
	&& cd /usr/src/python \
	&& ./configure --enable-shared --enable-unicode=ucs4 \
	&& make -j$(nproc) \
	&& make install \
	&& ldconfig \
	&& find /usr/local \
		\( -type d -a -name test -o -name tests \) \
		-o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
		-exec rm -rf '{}' + \
	&& rm -rf /usr/src/python

# make some useful symlinks that are expected to exist
RUN cd /usr/local/bin \
	&& ln -s easy_install-3.4 easy_install \
	&& ln -s idle3 idle \
	&& ln -s pip3 pip \
	&& ln -s pydoc3 pydoc \
	&& ln -s python3 python \
	&& ln -s python-config3 python-config

 RUN apt-get install -y python-psycopg2 libpq-dev
 RUN apt-get install -y supervisor
 RUN service supervisor stop
 RUN groupadd -r mediaTek \
  && useradd -r -g mediaTek mediaTek
 ADD requirements.txt /app/
 RUN /usr/local/bin/pip install -r requirements.txt
 RUN /usr/local/bin/pip install supervisor-stdout

 ADD deploy_tools/start-srv.sh /src/
 
ADD ./deploy_tools/supervisord.conf /etc/supervisor/conf.d/mediaTek.conf
 ADD ./deploy_tools/nginx.conf /etc/nginx/nginx.conf
 # restart nginx to load the config
 RUN service nginx stop

