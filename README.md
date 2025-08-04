# FastAPI Film Catalog

[![Python checks 🐍](https://github.com/yaros2106/FastAPI-Film-Catalog/actions/workflows/python-checks.yaml/badge.svg?branch=main)](https://github.com/yaros2106/FastAPI-Film-Catalog/actions/workflows/python-checks.yaml)

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
