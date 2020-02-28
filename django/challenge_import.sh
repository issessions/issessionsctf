#!/bin/bash
### USAGE ###
# NOTE: Quotes & commas will break this scripe
# example: ./challenge_import.sh challenges.csv
# This script takes one CSV file as an argument

#Removes first line of CSV file, and starts the import statments @ line 2
function import_csv {
	sed 1d $1 | while IFS=, read -r challenge_name developer_name description_file_name points link participant_zip_name deployement_zip_name hint hint_penalty flag category solution_file_name web_project docker
	do
		category=$(echo $category | awk '{ print toupper($0) }')
		psql -U postgres -h postgresql -d iss -c "INSERT INTO ctf_challenge (contest_id, name, description, category, link, file, active, dynamic_link, sponsored) values ('1', '$challenge_name', '$description_file_name', '$category', '$link', '$participant_zip_name', true, false, false) RETURNING ctf_challenge.id; INSERT INTO ctf_flag (name, flag, points, hint, penalty, solved, last_solved, challenge_id) VALUES ('$challenge_name', '$flag', '$points', '$hint',  '$hint_penalty', 0, NULL, currval('ctf_challenge_id_seq'))"
	done
}

start="NOW()"
end="(NOW() - INTERVAL '1 day')"
psql -U postgres -h postgresql -d iss -c "INSERT INTO ctf_contest values(1, 'contest_name', 't', $start::TIMESTAMPTZ, $end::TIMESTAMPTZ)"

for i in $(find /usr/src/app/ -name "*.csv"); do \
        import_csv $i; \
done
