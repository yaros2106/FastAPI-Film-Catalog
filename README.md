# FastAPI Film Catalog

[![Python checks 🐍](https://img.shields.io/github/actions/workflow/status/yaros2106/FastAPI-Film-Catalog/python-checks.yaml?branch=main&style=for-the-badge&label=Python%20checks%20%F0%9F%90%8D&labelColor=161b22&logo=github)](https://github.com/yaros2106/FastAPI-Film-Catalog/actions/workflows/python-checks.yaml)
[![Python](https://img.shields.io/badge/python-3.13+-blue?style=for-the-badge&logo=python&labelColor=161b22)](https://www.python.org/)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge&logo=python&logoColor=white&labelColor=161b22)](https://black.readthedocs.io/en/stable/)
[![Ruff](https://img.shields.io/badge/linter-ruff-%23ef5b25?style=for-the-badge&logo=ruff&logoColor=white&labelColor=161b22)](https://docs.astral.sh/ruff/)
[![Mypy](https://img.shields.io/badge/type%20checker-mypy-blueviolet?style=for-the-badge&logo=python&logoColor=white&labelColor=161b22)](http://mypy-lang.org/)
[![uv](https://img.shields.io/badge/installer-uv-4B8BBE?style=for-the-badge&logo=python&logoColor=white&labelColor=161b22)](https://github.com/astral-sh/uv)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge&logo=pre-commit&logoColor=white&labelColor=161b22)](https://pre-commit.com/)

## Develop

### Setup:

Right click `film-catalog` -> Mark Directory as -> Sources Root

### Install dependencies

Install all packages:
```shell
uv sync
```

### Configure pre-commit

Install pre-commit hook:
```shell
pre-commit install
```

### Run

Go to workdir:
```shell
cd film-catalog
```

Run dev server:
```shell
fastapi dev
```

## Snippets
```shell
python -c "import secrets;print(secrets.token_urlsafe(16))"
```
