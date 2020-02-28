psql -U postgres -v DB_NAME=$DB_NAME -v DB_USER=$DB_USER -v DB_PASS=$DB_PASS -v DB_ADDRES=$DB_ADDRES -v DB_PORT=$DB_PORT -f /home/create_user.sql
