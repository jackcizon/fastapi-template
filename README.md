![CI](https://github.com/jackcizon/fastapi-template/actions/workflows/ci.yaml/badge.svg)

# A Minium FastAPI Template Project

# Version

`3.0.0` (async)

## get the template project:

```bash
git clone https://github.com/jackcizon/fastapi-template.git
```

## del the useless parts:

```bash
cd fastapi-template
rm -rf .git
rm docs/*.md
rm -rf src/api/migrations
cd ..
mv fastapi-tempalte <your_project_name>
```

## before starting

- check TODO in `pycharm` and modify them
- edit conf in `envs/`
- edit docker in `docekr/`
- see some scripts in `scripts/`
- see cli by `python manage.py Demo`

## init db

```shell
python manage.py AlembicInit
```

in `src/api/migrations/env.py`

```python
# from

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# to

from src.core.database import Base
from src.api.models import *  # must include

target_metadata = Base.metadata
```

# start project

```shell
python manage.py AlembicCheck
python manage.py MakeMigrations
python manage.py Migrate

# if there are some issues, remember to `del all` records/rows in table:`alembic_version`.

python manage.py BatchCreateRoles
python manage.py BatchUpdatePermissions
python manage.py RunServer
```

## Test

```shell
python manage.py RunTests
# or
# make test
```
