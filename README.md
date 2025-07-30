# FastAPI Film Catalog

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
