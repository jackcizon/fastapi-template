# 文件在 root/scripts/ 下
docker compose \
  --env-file ../envs/.env.dev.infra \
  -f ../docker/compose.yaml \
  up -d
