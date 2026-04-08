```shell
mkdir docs
cd docs
sphinx-quickstart
cd ..
poetry add python-docs-theme
sphinx-autobuild docs docs/_build/html
```