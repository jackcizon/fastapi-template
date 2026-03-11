# please modify vars in envs before running this scripts.
docker compose \
  --env-file ../envs/.env.docker.dev \
  -f ../docker/compose.yaml \
  up -d
