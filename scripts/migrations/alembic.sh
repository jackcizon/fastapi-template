alembic init src/api/migrations
alembic check
alembic revision --autogenerate --version-path src/api/migrations/versions -m ""
alembic upgrade head
