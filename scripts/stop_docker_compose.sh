# 文件在 root/scripts/ 下
docker compose \
  --env-file ../envs/.env.dev \
  -f ../docker/compose.yaml \
  down
