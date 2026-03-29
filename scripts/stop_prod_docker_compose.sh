docker compose \
  --env-file ../envs/.env.docker.prod \
  -f ../docker/compose.prod.yaml \
  down # -v