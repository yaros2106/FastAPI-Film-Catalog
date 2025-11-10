# 🎞️ FastAPI Film Catalog

A FastAPI-based application for managing and browsing a film catalog. Designed with scalability and developer experience in mind.

[![Python checks 🐍](https://img.shields.io/github/actions/workflow/status/yaros2106/FastAPI-Film-Catalog/python-checks.yaml?branch=main&style=for-the-badge&label=Python%20checks%20%F0%9F%90%8D&labelColor=161b22&logo=github)](https://github.com/yaros2106/FastAPI-Film-Catalog/actions/workflows/python-checks.yaml)
[![Python](https://img.shields.io/badge/python-3.13+-blue?style=for-the-badge&logo=python&labelColor=161b22)](https://www.python.org/)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge&logo=python&logoColor=white&labelColor=161b22)](https://black.readthedocs.io/en/stable/)
[![Ruff](https://img.shields.io/badge/linter-ruff-%23ef5b25?style=for-the-badge&logo=ruff&logoColor=white&labelColor=161b22)](https://docs.astral.sh/ruff/)
[![Mypy](https://img.shields.io/badge/type%20checker-mypy-blueviolet?style=for-the-badge&logo=python&logoColor=white&labelColor=161b22)](http://mypy-lang.org/)
[![uv](https://img.shields.io/badge/installer-uv-4B8BBE?style=for-the-badge&logo=python&logoColor=white&labelColor=161b22)](https://github.com/astral-sh/uv)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge&logo=pre-commit&logoColor=white&labelColor=161b22)](https://pre-commit.com/)
[![Coverage](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2Fyaros2106%2F9dd79657afe76d52e3a70bd197475d42%2Fraw%2Fcoverage.json&style=for-the-badge&color=brightgreen&labelColor=161b22)](https://github.com/yaros2106/FastAPI-Film-Catalog/actions/workflows/python-checks.yaml)

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/yaros2106/FastAPI-Film-Catalog/main.svg)](https://results.pre-commit.ci/latest/github/yaros2106/FastAPI-Film-Catalog/main)
[![Coverage](https://codecov.io/gh/yaros2106/FastAPI-Film-Catalog/branch/main/graph/badge.svg?style=for-the-badge&labelColor=2d2f36)](https://codecov.io/gh/yaros2106/FastAPI-Film-Catalog)

---

## 🚀 Features

- FastAPI-powered backend
- REST API for movies
- Async support
- Integrated testing setup
- Pre-commit hooks for clean code
- Redis support (for caching or other async tasks)

---

## 🧑‍💻 Getting Started

### 🛠️ Setup:

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/film-catalog.git
    cd film-catalog
    ```

2. Right click `film-catalog` -> Mark Directory as -> Sources Root

### 📦 Install dependencies

Use [`uv`](https://github.com/astral-sh/uv) to install packages:
```shell
  uv sync
```

### ⚙️ Configuration `.env` file

The application requires environment variables to work.
Copy the `.env.template` file to `.env` and specify your values:
```shell
cp .env.template .env
```

### ⚙️ Configure pre-commit

Install pre-commit hook:
```shell
  pre-commit install
```

### 🚀 Run Development Server

1. Go to workdir:
    ```shell
    cd film-catalog
    ```

2. Make sure Redis is running:

    ```bash
    docker run -d -p 6379:6379 redis
    ```

3. Start the FastAPI dev server:

    ```bash
    fastapi dev
    ```

The server will be available at `http://localhost:8000`.

---

### ✅ Running Tests

1. Make sure that the Redis test container is running.:

```bash
  docker run -d -p 6380:6380 redis
```
2. Set the required environment variables before running tests or starting the dev server:

**PowerShell**:
```powershell
  $env:TESTING = "1"
  $env:REDIS_PORT = "6380"
```


**Bash**:
```bash
  export TESTING=1
  export REDIS_PORT=6380
```

3. Run the test suite:

```bash
  python -m unittest -v
```
   or with coverage
```bash
  coverage run -m unittest
```

---


### 🧪 Useful Snippets

Generate a random secret key:

```shell
  python -c "import secrets;print(secrets.token_urlsafe(16))"
```

---

## 👨‍🔧 For Developers

* Use a virtual environment (`uv`, `venv`, or `poetry`) to manage dependencies.
* Follow PEP8 style guidelines (auto-enforced via `pre-commit`).
* Use descriptive commit messages (consider [Conventional Commits](https://www.conventionalcommits.org/)).
* Document public endpoints and services clearly with docstrings and OpenAPI schemas.

---
