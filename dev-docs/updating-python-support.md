# Updating Python Support

This file documents how to add a new python version and/or remove an old one to automated testing and GitHub CI.

To add python 3.13 & remove python 3.9:


Files to update:

- tox.ini
  - replace all cases of `39,310,311,312` with `310,311,312,313`
- setup.py
  - update minimum python: `python_requires='>=3.10'`
  - update `classifiers`:

    ```"Programming Language :: Python :: 3.13"```
- Docker:
  - rename py39.Dockerfile to py313.Dockerfile
    - replace '3.9' with '3.13' globally
    - replace 'py39' with 'py313' globally
  - `clean.sh`
    - add `docker_py313` to `docker image rm` command
    - it's okay to leave `docker_py39` to ensure it gets removed
    - If there's a really old docker python image, e.g., `docker_py38`, go ahead and remove that
  - `build.sh`
    - copy 'docker buildx' command for python 3.12
      - replace all `py312` with `py313`
    - delete `docker buildx` command for python 3.9
  - `run.sh`
    - duplicate run command for `docker_py312`, replacing container name with `docker_py313`
    - delete `docker run` command for python 3.9
  - `run-individual.sh`
    - duplicate `elif` clause for python 3.12, updating it to `docker_py312`
    - delete `if-elif` clause for python 3.9
    - update help message: `"Specify py310, py311, py312, or py313"`
- rennovate.json
  - add dict for 3.13 dockerfile
  - Note the name of the dockerfile, as well as `allowedVersions` key:
  ```
  {
    "matchPaths": ["docker_testing/docker/py313.Dockerfile"],
    "matchPackageNames":["python"],
    "allowedVersions": "3.13"
  }
  ```
  - remove dict for 3.9
- .github/workflows/testing-linting.yml
  - update python version matrix: `["3.10", "3.11", "3.12", "3.13"]`
- _readme_template.md
  - Update minimum python version under requirements
- README.md:
  - run `scripts/update_readme.py` to apply changes to README.md
