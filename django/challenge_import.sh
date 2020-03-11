#!/bin/bash
### USAGE ###
# NOTE: Quotes & commas will break this scripe
# example: ./challenge_import.sh
# This script takes any # of csv files in the directory /usr/src/app or ./django on the host and imports them into the database

#Removes first line of CSV file, and starts the import statments @ line 2
function import_csv {
	sed 1d $1 | while IFS=, read -r challengeid challenge_name developer_name description_file_name points link participant_zip_name deployement_zip_name hint hint_penalty flag category solution_file_name web_project docker
	do
		category=$(echo $category | awk '{ print tolower($0) }')
		if echo $link | grep -i "n/a" > /dev/null; then
			link=""
		fi
		description_file_content=$(cat $2/$challengeid/$description_file_name)
		hint_content=$(cat $2/$challengeid/$hint)
		solution_file_name_content=$(cat $2/$challengeid/$solution_file_name)

		PGPASSWORD=$DB_PASS
		psql -U $DB_USER -h $DB_ADDRESS -d $DB_NAME -c "INSERT INTO ctf_challenge (contest_id, name, description, category, link, file, minio_file_id, challenge_id, active, dynamic_link, sponsored) values ('1', '$challenge_name', '$description_file_content', '$category', '$link', '$participant_zip_name', 'MintoFileId?', '$challengeid', true, false, false) RETURNING ctf_challenge.id; INSERT INTO ctf_flag (name, flag, points, hint, penalty, solved, last_solved, challenge_id) VALUES ('$challenge_name', '$flag', '$points', '$hint_content',  '$hint_penalty', 0, NULL, currval('ctf_challenge_id_seq'))"
	done
}

contest_created=0
if [ $(find /usr/src/app/ -name "*.zip") ]; then
#for i in $(find /usr/src/app/ -name "*.csv"); do
	if [[ $CREATE_CONTEST == 1 && $contest_created == 0 ]]; then
		echo "Creating Contest Name: $CONTEST_NAME"
		#Creates contest, in order for challenge imports to work there needed to be a contest with the ID of 1
		PGPASSWORD=$DB_PASS
		psql -U $DB_USER -h $DB_ADDRESS -d $DB_NAME -c "INSERT INTO ctf_contest values(1, '$CONTEST_NAME', '$CONTEST_ACTIVE', $CONTEST_START::TIMESTAMPTZ, $CONTEST_END::TIMESTAMPTZ)"
		contest_created=1
	fi
	challenge_folder=$(find /usr/src/app/ -name "*.zip" | sed 's/.zip//g')
	unzip $(find /usr/src/app/ -name "*.zip")
	for i in $(find $challenge_folder -name "*.csv"); do
        	import_csv $i $challenge_folder;
	done
fi
