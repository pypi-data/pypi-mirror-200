[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Preface

This is the closed-source Testmon. The repo has a couple of subprojects:

1. **testmon_dev**: the server, it has normal change code/execute cycle which we're used to when developing in Python.
   open source testmon (**OSPT**) is generated from here (via preprocess). Main package is called testmon_dev, and it is
   installed via  `pip install -r requirements/prod.txt -e .`

1. **Open Source Testmon (OSPT)**: This is the opensource pytest-testmon released to
   PYPI, attracts new users. It's generated from testmon-dev, comments and type hints are stripped out.
   Tests are also generated and executed via tox for a couple of combinations of dependencies and python
   versions, but they are not published. [Release process of OSPT ](docs/ospt_release.md)

We generate pytest-testmon by running [preprocess](https://pypi.org/project/preprocess/) on the source.
`preprocess` template directives are in Python comments so testmon_dev can be executed as is and is the template for
pytest-testmon.

# [Process](docs/process.md)


# Installation and tests

Have a look at [.github/workflows/tests.yml](.github/workflows/tests.yml) to see how CI is set up and what are the prerequisites.
(e.g. Python 3.7 and 3.11)

You should clone this repo (https://github.com/tarpas/testmon-dev/) and 2 additional ones. If you only clone
testmon-dev initially you can still build, but you'll have to come back to this set-up when you will want to
push to one of the other repos.

```
git clone https://github.com/tarpas/testmon-dev/
git clone https://github.com/tarpas/pytest-testmon/
git clone https://github.com/tarpas/testmon.org/
git clone https://github.com/tarpas/testmon_web/
```

The build in testmon-dev also generates files into other directories: pytest-testmon (open source) and testmon.org (
pelican site source) on the same level.

```
cd testmon-dev

# create and activate virtualenv (e.g. python -m venv .venv)

pip install -r requirements/prod.txt -e .

# increase ulimit if needed
ulimit -n 1024

# run tests
pytest

# build pytest-testmon and run it's test suite (tox)
python tools/build/build.py testmon
cd ../pytest-testmon
tox
```

# Contributing

1. We use pre-commit so run `pre-commit install` and `pre-commit install-hooks` before commiting.
1. Run tests (pytest).
5. Build pytest-testmon `python tools/build/build.py testmon` and run it's test suite `cd ..;cd pytest-testmon;tox`

See also [process](docs/process.md)

# Data model

## Current denormalized schema (client):
[Described in file 'docs/schema_client.md'](docs/schema_client.md)

## Current denormalized schema (client):
[Described in file 'docs/schema_server.md'](docs/schema_server.md)

# runtime environments

- development (and build, test, lint)
    - local dogfooding is possible (running the test suite with pytest —testmon)
- CI - GHA
- client installations in the wild - open source pytest-tesmon, distributed via PYPI without comments and types. Tested
  with comprehensive test suite which is executed in many combinations of dependencies via tox and GHA(windows/linux),
  but the tests are not published
- server
- performance regression tests via valgrind cachegrind (see Dockerfile and tools/benchmark.py)

# performance testing/benchmarking

```
    docker build . --platform=linux/arm64 -t testmon -f Dockerfile.perf-benchmark
    docker run -it -v "$(pwd)":/mount -t testmon
```
# Fly deployment
## automatically

git reset --hard the `deploy` branch to the commit you want to deploy and `push --force` it to the tarpas/testmon-dev repo. There is a GH [action](.github/workflows/fly.yml) which automatically deploys.

## manually
```
fly deploy
```