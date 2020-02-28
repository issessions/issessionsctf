#!/bin/bash
### USAGE ###
# NOTE: Quotes & commas will break this scripe
# example: ./challenge_import.sh
# This script takes any # of csv files in the directory /usr/src/app or ./django on the host and imports them into the database

#Removes first line of CSV file, and starts the import statments @ line 2
function import_csv {
	sed 1d $1 | while IFS=, read -r challenge_name developer_name description_file_name points link participant_zip_name deployement_zip_name hint hint_penalty flag category solution_file_name web_project docker
	do
		category=$(echo $category | awk '{ print toupper($0) }')
		psql -U postgres -h postgresql -d iss -c "INSERT INTO ctf_challenge (contest_id, name, description, category, link, file, active, dynamic_link, sponsored) values ('1', '$challenge_name', '$description_file_name', '$category', '$link', '$participant_zip_name', true, false, false) RETURNING ctf_challenge.id; INSERT INTO ctf_flag (name, flag, points, hint, penalty, solved, last_solved, challenge_id) VALUES ('$challenge_name', '$flag', '$points', '$hint',  '$hint_penalty', 0, NULL, currval('ctf_challenge_id_seq'))"
	done
}

contest_created=0
for i in $(find /usr/src/app/ -name "*.csv"); do
	if [ $contest_created == 0 ]; then
		#Creates contest, in order for challenge imports to work there needed to be a contest with the ID of 1
		psql -U postgres -h postgresql -d iss -c "INSERT INTO ctf_contest values(1, '$CONTEST_NAME', '$CONTEST_ACTIVE', $CONTEST_START::TIMESTAMPTZ, $CONTEST_END::TIMESTAMPTZ)"
		contest_created=1
	fi
        import_csv $i;
done
