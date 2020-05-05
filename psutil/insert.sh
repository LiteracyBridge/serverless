#!/usr/bin/env bash
traditionalIFS="$IFS"
#IFS="`printf '\n\t'`"
set -u

# Script to create and initially populate the recipients table.

if [ -z "${psql:-}" ]; then
    if [ -e /Applications/Postgres.app/Contents/Versions/9.5/bin/psql ]; then
        psql=/Applications/Postgres.app/Contents/Versions/9.5/bin/psql
    elif [ -e /Applications/Postgres.app/Contents/Versions/9.4/bin/psql ]; then
        psql=/Applications/Postgres.app/Contents/Versions/9.4/bin/psql
    elif [ ! -z "$(which psql)" ]; then
        psql=$(which psql)
    else
        echo "Can't find psql!"
        exit 100
    fi
fi
if [ -z "${dbcxn:-}" ]; then
    dbcxn=" --host=lb-device-usage.ccekjtcevhb7.us-west-2.rds.amazonaws.com --port 5432 --username=lb_data_uploader --dbname=dashboard "
    # dbcxn="--host=localhost --port=5432 --username=lb_data_uploader --dbname=dashboard"

fi

function configure() {
    recipientsfile="recipients.csv"
    recipmapfile="recipients_map.csv"
    deplspecfile="deployment_spec.csv"

    project="$(awk -F , 'NR==2{print $2}' recipients.csv)"

    echo $(date)>log.txt
    echo "Program is ${project}">>log.txt
    verbose=true
    execute=true

    echo "psql: ${psql}"
    echo "dbcxn: ${dbcxn}"
}

function main() {
    configure

    set -x
    
    importTable
}



function importTable() {
    # Import into db, and update recipients
    ${psql} ${dbcxn} -a <<EndOfQuery >>log.txt
    \\timing
    \\set ECHO all
    CREATE TEMPORARY TABLE temp_recip AS SELECT * FROM recipients WHERE FALSE;
    \copy temp_recip from '${recipientsfile}' with delimiter ',' csv header;
    INSERT INTO recipients SELECT * FROM temp_recip
        ON CONFLICT DO NOTHING;
    UPDATE recipients SET communityname = t.communityname,
                          groupname = t.groupname,
                          affiliate = t.affiliate,
                          component = t.component,
                          country = t.country,
                          region = t.region,
                          district = t.district,
                          numhouseholds = t.numhouseholds,
                          numtbs = t.numtbs,
                          supportentity = t.supportentity,
                          model = t.model,
                          language = t.language,
                          coordinates = t.coordinates,
                          agent = t.agent,
                          latitude = t.latitude,
                          longitude = t.longitude
            FROM temp_recip t
            WHERE recipients.recipientid = t.recipientid;

    SELECT * FROM recipients WHERE project='${project}';

    CREATE TEMPORARY TABLE temp_recip_map AS SELECT * FROM recipients_map WHERE FALSE;
    \copy temp_recip_map from '${recipmapfile}' with delimiter ',' csv header;
    INSERT INTO recipients_map SELECT * FROM temp_recip_map  
        ON CONFLICT DO NOTHING;

    SELECT * FROM recipients_map WHERE project='${project}';

    CREATE TEMPORARY TABLE temp_deployments (
        project CHARACTER VARYING,
        deployment_num INTEGER,
        startdate DATE,
        enddate DATE,
        component CHARACTER VARYING,
        name CHARACTER VARYING
        );
    \copy temp_deployments from '${deplspecfile}' with delimiter ',' csv header;
    UPDATE temp_deployments SET component='' WHERE component IS NULL;
    INSERT INTO deployments
        SELECT project, name, name, deployment_num, startdate, enddate, '', '', component
        FROM temp_deployments
        ON CONFLICT DO NOTHING;
    UPDATE deployments SET startdate = d.startdate,
                           enddate = d.enddate,
                           component = d.component
            FROM temp_deployments d
            WHERE deployments.project = '${project}' AND deployments.deploymentnumber = d.deployment_num;

    SELECT * FROM deployments WHERE project = '${project}' ORDER BY deploymentnumber;

EndOfQuery
}

main "$@"

# ta-da

