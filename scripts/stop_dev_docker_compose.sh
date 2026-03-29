# please modify vars in envs before running this script.
docker compose \
  --env-file ../envs/.env.docker.dev \
  -f ../docker/compose.dev.yaml \
  down # -v