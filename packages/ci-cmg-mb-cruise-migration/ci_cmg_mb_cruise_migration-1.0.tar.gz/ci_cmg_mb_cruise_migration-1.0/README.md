# mb-cruise-migration

Migration scripts for migrating multibeam metadata from MB schema to CRUISE schema. 

## Usage: Migration Instructions
Migration can be run one of two ways. 
In both cases, a config file must be provided. 
In both cases, a virtualenv will need to be setup. Directions below. 

1. Pulling down project from Github repo, updating the config, and running the provided `run.sh` or `start_background.sh` script. 
2. Importing the `ci-cmg-mb-cruise-migration` package into a python run script and creating an instance of the "Migrator" class, 
passing in the path to a config file as the only parameter, then running the "migrate" method on class.
   * Use of a run script modeled after the provided run scripts to run python script in background is recommended.  
   * The package and it's dependencies will need to be installed prior to usage. This can be done in virtual environment with `python -m pip install ci-cmg-mb-cruise-migration`. 

NOTE: if enabling pooled connections for cruise db in config, oracle client libraries need to be installed:
https://python-oracledb.readthedocs.io/en/latest/user_guide/installation.html#optionally-install-oracle-client

## Developing Project

### Setup virtual environment

1. setup virtualenv
2. specify python installation for virtualenv to use
3. activate the virtual environment
4. verify python version and virtualenv
5. install required modules
6. verify they were installed with pip list
7. deactivate the virtual environment

```bash
virtualenv migenv

virtualenv --python=</path/to/python> </path/to/new/virtualenv/>

source ./migenv/bin/activate

python which
python -V

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

pip list

deactivate
```


### run tests 

Many (most) tests are integration tests and require either one or both the MB or CRUISE schema docker
containers be running.

To start docker containers:
from test dir:
```bash
./start-it.sh
```

To run tests:
from project root:
```bash
python -m unittest discover tests
```

To stop docker containers:
from test dir:
```bash
./stop-it.sh
```

### build project

1. Update version in pyproject.toml either before or after release.
2. If not already installed: `python -m pip install --upgrade build`
3. Build distribution: `python -m build`
4. If not already installed: `python -m pip install --upgrade twine`
5. Upload to pypi: `twine upload dist/*`
