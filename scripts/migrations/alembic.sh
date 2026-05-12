alembic init src/core/db/migrations
alembic check
alembic revision --autogenerate --version-path src/core/db/migrations/versions -m ""
alembic upgrade head
