# 📘 CONTRIBUTING.md

This document explains how our team collaborates using **GitHub**, **feature branches**, **pull requests**, **pre-commit hooks**, and **GitHub Actions CI**.
All contributors must follow this workflow.

Here's a summary of the steps needed to contribute.
For further details, keep on reading.

---

# ✔  Summary: steps to contribute

To contribute:

0. Clone SUSI and install the dev environment
1. Create a branch
2. Modify the code in the new branch. (Write new tests, if possible!)
3. Run tests
4. Commit the changes to the new branch. `pre-commit` will run automatically and format the code
4. Push your branch
5. Open a Pull Request (PR)
6. Continuous Integration (CI) will run in GitHub's servers
7. We will review the PR
8. If successful, we will merge it

---

# Install SUSI dev environment
You only need to follow these steps once.

1. Clone the latest version of the code.
```bash
git clone <repo-url>
```
2. Navigate into the project folder and install the python environment.
```bash
uv sync
```
(You need the [`uv`](https://docs.astral.sh/uv/getting-started/installation/)  python package and environment manager)


3. Install the pre-commit hooks (more info on this below)
```bash
pre-commit install
```
You're ready!

(Tip: Since we use **[ruff](https://docs.astral.sh/ruff/)** to format the code, you might consider installng it in your favourite IDE for a better developer experience.)

---

# 🔀 Git Workflow: Feature/Branch

* The `main` branch is **always stable**.
* Every contribution occurs on a feature branch. This means that if you want to add or modify some code, you must create a new branch.
* No commits go directly to `main`. Instead, Pull Requests are created so that every change to `main` is reviewable.

## Branch naming conventions

```
feature/<short-description>
bugfix/<issue-or-description>
refactor/<scope>
```
- Feature: new code behaviour.
- Bugfix: no new behaviour, just fix something that was broken.
- Refactor: no new behaviour, just move things around.

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
Now you can make the changes you want, this won't affect the `main` branch.



---

# 🧹 pre-commit: Code Formatting Standards

We enforce formatting, linting, import cleanup, and notebook hygiene via **pre-commit**.

The tools we use are:
* **ruff** - Code formatting and linting
* **nbstripout** – Remove notebook outputs

This means that before you run `git commit`, those tools below will review and attempt to format the code.
If they can do the formatting automatically, they will.
If they cannot, you will need to fix the errors manually.

Your code **must** pass all checks before being pushed.


Note that you can also run pre-commit manually:
```bash
pre-commit run --all-files
```

This is configured in the `.pre-commit-config.yaml` file.

---

# 🧪 Testing

We use **pytest** for automated tests.
Run tests locally:

```bash
uv run pytest
```
Or, if your `venv` is activated:

```bash
pytest
```

All tests must pass before submitting a Pull Request.
(This is enforced automatically by the CI with GitHub Actions, see below).

---

# 🔄 Pull Requests (PR)

Every merge into `main` happens through a Pull Request.
You cannot `push` directly to the `main` branch.

### PR Requirements

* All pre-commit checks pass
* All CI checks pass
* Small, focused PRs
* Good title and description
* Ideally, tests are included for new functionality

---

# 🚀 CI (GitHub Actions)

Continuous Integration (CI) runs automatically on Pull Requests and on pushes to `main`.
CI checks:

* ruff
* pytest

If CI fails, the PR **cannot** be merged.

This is configured in the `.github/workflows/ci.yaml` file.


