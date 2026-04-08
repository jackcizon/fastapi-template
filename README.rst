A Minimum FastAPI Template Project
==================================

.. image:: https://github.com/jackcizon/fastapi-template/actions/workflows/ci.yaml/badge.svg
   :target: https://github.com/jackcizon/fastapi-template/actions/workflows/ci.yaml
   :alt: CI


Version
-------

``3.0.2`` (async)

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
    rm -rf src/api/migrations
    cd ..
    mv fastapi-template <your_project_name>

Before starting
---------------

* Check **TODO** in PyCharm and modify them.
* Edit config files in ``envs/``.
* Edit Docker configurations in ``docker/``.
* See available scripts in ``scripts/``.
* View CLI usage: ``python manage.py Demo``.

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

    from src.core.database import Base
    from src.api.models import * # must include

    target_metadata = Base.metadata

Start project
-------------

.. code-block:: shell

    python manage.py AlembicCheck
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