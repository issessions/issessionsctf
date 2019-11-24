CREATE DATABASE iss;
CREATE USER issessions;
ALTER USER issessions WITH PASSWORD 'issessions';
ALTER ROLE issessions with login;
ALTER ROLE issessions with superuser;

