# please modify vars in envs before running this script.
docker compose \
  --env-file ../envs/.env.docker.dev \
  -f ../docker/compose.yaml \
  up -d
