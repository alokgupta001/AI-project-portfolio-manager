#!/bin/sh
set -eu
psql --username postgres --dbname postgres --set ON_ERROR_STOP=1 \
  --set owner_password="$PPM_OWNER_PASSWORD" --set app_password="$PPM_APP_PASSWORD" <<'SQL'
CREATE ROLE ppm_owner LOGIN PASSWORD :'owner_password' NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS;
CREATE ROLE ppm_app LOGIN PASSWORD :'app_password' NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS;
ALTER DATABASE ppm_local OWNER TO ppm_owner;
CREATE DATABASE ppm_test OWNER ppm_owner;
CREATE DATABASE ppm_demo OWNER ppm_owner;
REVOKE CONNECT ON DATABASE ppm_local, ppm_test, ppm_demo FROM PUBLIC;
GRANT CONNECT ON DATABASE ppm_local, ppm_test, ppm_demo TO ppm_owner, ppm_app;
SQL
for database in ppm_local ppm_test ppm_demo; do
  psql --username postgres --dbname "$database" --set ON_ERROR_STOP=1 <<'SQL'
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
GRANT USAGE, CREATE ON SCHEMA public TO ppm_owner;
GRANT USAGE ON SCHEMA public TO ppm_app;
ALTER DEFAULT PRIVILEGES FOR ROLE ppm_owner IN SCHEMA public GRANT SELECT ON TABLES TO ppm_app;
SQL
done
