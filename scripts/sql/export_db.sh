# in shell
#docker exec -it postgresql_fastapi_template /bin/sh

# in docker shell
#pg_dump -U jack -h 192.168.8.7 -p 5432 -F p -f fastapi_template.sql fastapi_template

# copy container:/path/to/file /path/to/host_machine
docker cp postgresql_fastapi_template:/fastapi_template.sql ./fastapi_template.sql
