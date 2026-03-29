docker compose \
  --env-file ../envs/.env.docker.test \
  -f ../docker/compose.test.yaml \
  up -d \
  --remove-orphans
