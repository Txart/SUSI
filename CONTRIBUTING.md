# 📘 CONTRIBUTING.md

This document explains how our team collaborates using **GitHub**, **feature branches**, **pull requests**, **pre-commit hooks**, and **GitHub Actions CI**.
All contributors must follow this workflow.

---
# Install SUSI
We use [`uv`](https://docs.astral.sh/uv/getting-started/installation/) to set the directory and manage packages.

```bash
uv 
```


---

# 🔀 Git Workflow: Feature/Branch

* The `main` branch is **always stable**.
* Every contribution occurs on a feature branch. Which means that if you want to add a feature, you must create a new branch.
* No commits go directly to `main`. Instead, Pull Requests are created so that every change to `main` is reviewable.

## Branch naming

```
feature/<short-description>
bugfix/<issue-or-description>
refactor/<scope>
```
- Feature: new code behaviour
- Bugfix: no new behaviour, just fix something that was broken
- Refactor: no new behaviour, just move things around

**Examples:**

```
feature/add-simulation-runner
bugfix/fix-numpy-shape-error
```

---

# 📥 How to Start Working

1. Create a branch from `main`:

```bash
git switch main    # ensure you are in main
git pull    # get latest version of the code
git switch -c feature/my-feature    # create a new branch and switch to it
```

2. Install dependencies:


3. Install pre-commit hooks:

```bash
pip install pre-commit
pre-commit install
```

---

# 🧹 Code Quality Standards

We enforce formatting, linting, import cleanup, and notebook hygiene via **pre-commit**.

Running manually (optional):

```bash
pre-commit run --all-files
```

## Tools we use

* **black** – Consistent formatting
* **isort** – Import sorting
* **flake8** – Lint checks
* **mypy** (optional) – Type checking
* **nbstripout** – Remove notebook outputs
* **detect-secrets** – Prevent committing secrets

Your code **must** pass all checks before being pushed.

---

# 🧪 Testing

We use **pytest** for automated tests.
Run tests locally:

```bash
pytest
```

All tests must pass before submitting a PR.

---

# 🔄 Pull Requests

Every merge into `main` happens through a Pull Request.

### PR Requirements

* Small, focused PRs
* Good title and description
* Tests are included for new functionality
* All pre-commit checks pass
* All CI checks pass

### PR Review Expectations

Reviewers check for:

* correctness
* readable, maintainable code
* appropriate documentation and docstrings
* passing tests and linters

---

# 🚀 CI (GitHub Actions)

CI runs automatically on Pull Requests and on pushes to `main`.
CI checks:

* black formatting
* isort
* flake8
* pytest

If CI fails, the PR **cannot** be merged.

---

# 📁 Project Structure

A typical project layout:

```
project/
├── src/
│   └── project_name/
├── tests/
├── notebooks/
├── requirements.txt
├── pyproject.toml
├── .pre-commit-config.yaml
└── .github/workflows/ci.yaml
```

---

# ✔ Summary

To contribute:

1. Create a feature branch
2. Install and use pre-commit
3. Write & run tests
4. Push your branch
5. Open a Pull Request
6. Pass review + CI
7. Merge

---

# `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-yaml
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: check-merge-conflict

  - repo: https://github.com/psf/black
    rev: 24.3.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/PyCQA/isort
    rev: 5.13.2
    hooks:
      - id: isort

  - repo: https://github.com/PyCQA/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        additional_dependencies: [flake8-bugbear]

  - repo: https://github.com/nbQA-dev/nbQA
    rev: 1.8.4
    hooks:
      - id: nbqa-black
      - id: nbqa-isort
      - id: nbqa-flake8

  - repo: https://github.com/kynan/nbstripout
    rev: 0.6.1
    hooks:
      - id: nbstripout

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
```

---

# `.github/workflows/ci.yaml`

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: "3.10"

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install black isort flake8 pytest

    - name: Run black
      run: black --check .

    - name: Run isort
      run: isort --check-only .

    - name: Run flake8
      run: flake8 .

    - name: Run tests
      run: pytest --maxfail=1 --disable-warnings
```

---

This completes the **CONTRIBUTING.md**, **pre‑commit configuration**, and **CI workflow**.
