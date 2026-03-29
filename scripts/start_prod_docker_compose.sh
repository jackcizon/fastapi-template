# please modify vars in envs before running this script.
docker compose \
  --env-file ../envs/.env.docker.prod \
  -f ../docker/compose.prod.yaml \
  up -d