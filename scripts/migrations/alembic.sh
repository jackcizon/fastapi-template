alembic init src/apps/migrations
alembic check
alembic revision --autogenerate --version-path src/apps/migrations/versions -m ""
alembic upgrade head
