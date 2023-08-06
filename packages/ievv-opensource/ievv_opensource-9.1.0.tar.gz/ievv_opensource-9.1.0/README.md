# ievv_opensource

## Develop
Requires:
- https://github.com/pyenv/pyenv
- Docker (Docker desktop or similar)


### Install for development

Install a local python version with pyenv:
```
$ pyenv install 3.10
$ pyenv local 3.10
```

Install dependencies in a virtualenv:
```
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install ".[dev,optional]"
```

### Run postgres and redis
```
$ docker-compose up
```

### Run dev server
```
$ source .venv/bin/activate   # enable virtualenv
$ ievv devrun -n docker-compose
```

### Run tests
```
$ source .venv/bin/activate   # enable virtualenv
$ pytest
```


### Destroy postgres and redis
```
$ docker-compose down -v
```


## Documentation
http://ievv-opensource.readthedocs.org/


## How to release ievv_opensource
1. Update version using `hatch version`:
   ```
   Major version update:
   $ hatch version major
   
   Minor version update:
   $ hatch version minor
   
   Patch version update:
   $ hatch version patch
   ```
2. Add releasenote to releasenotes folder on root with name `releasenotes-<major-version>.md`.
3. Commit with ``Release <version>``.
4. Tag the commit with ``<version>``.
5. Push (``git push && git push --tags``).
6. Release to pypi:
   ```
   $ hatch build -t sdist
   $ hatch publish
   ```
