CREATE DATABASE $DB_NAME;
CREATE USER $DB_USER;
ALTER USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
ALTER ROLE $DB_USER with login;
ALTER ROLE $DB_USER with superuser;

