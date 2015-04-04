#!/bin/bash

: ${DB_USER:=db_user}
: ${DB_PASSWORD:=db_pass}
: ${DB_NAME:=db_name}
: ${DB_ENCODING:=UTF-8}
gosu postgres postgres --single <<-EOSQL
    CREATE USER mediatek WITH PASSWORD 'mediatek';
    CREATE DATABASE mediatek;
    GRANT ALL PRIVILEGES ON DATABASE mediatek TO mediatek;
	ALTER USER mediatek CREATEDB;
EOSQL

