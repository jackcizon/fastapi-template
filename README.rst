A Minimum FastAPI Template Project
==================================

.. image:: https://github.com/jackcizon/fastapi-template/actions/workflows/ci.yaml/badge.svg
   :target: https://github.com/jackcizon/fastapi-template/actions/workflows/ci.yaml
   :alt: CI


Version
-------

``3.2.0`` (async)

Get the template project
------------------------

.. code-block:: bash

    git clone https://github.com/jackcizon/fastapi-template.git

Delete the useless parts
------------------------

.. code-block:: bash

    cd fastapi-template
    rm -rf .git
    rm docs/*.md
    rm -rf src/api/migrations  # must do this, otherwise `db init` operation will fail.
    cd ..
    mv fastapi-template <your_project_name>
    cd docs
    mkdir _static  # if _static not exists

Before starting
---------------

* Check **TODO** in PyCharm and modify them.
* Edit config files in ``envs/``.
* Edit Docker configurations in ``docker/``.
* See available scripts in ``scripts/``.
* View CLI usage: ``python manage.py Demo``.
* press ``ctrl+shift+r`` in PyCharm, find ``fastapi[_-]template``, and `192.168.8.7`, replace with your conf.
* ``poetry update`` to update deps, or use ``uv`` (maybe you like it, I prefer to ``poetry``).

Init DB
-------

.. code-block:: shell

    python manage.py AlembicInit

In file ``src/api/migrations/env.py``, modify the metadata configuration:

**From:**

.. code-block:: python

    # add your model's MetaData object here
    # for 'autogenerate' support
    # from myapp import mymodel
    # target_metadata = mymodel.Base.metadata
    target_metadata = None

**To:**

.. code-block:: python

    from src.core.db.models import Base
    from src.api.models import *  # must include

    target_metadata = Base.metadata

Start project
-------------

.. code-block:: shell

    python manage.py AlembicCheck
    # show error is ok
	# it means `alembic` notifies you that the models have changed,
	# but the migration has not yet occurred.
    python manage.py MakeMigrations
    python manage.py Migrate

.. note::
    If there are some issues, remember to **delete all** records/rows in table: ``alembic_version``.

.. code-block:: shell

    python manage.py BatchCreateRoles
    python manage.py BatchUpdatePermissions
    python manage.py RunServer

Test
----

.. code-block:: shell

    python manage.py RunTests
    # or
    # make test