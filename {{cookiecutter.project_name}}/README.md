# {{ cookiecutter.project_name }}

## Authors
{{ cookiecutter.app_developer }}

## Implementation language
python {{ cookiecutter.app_lang_version }}

## Deployment environment
Kubernetes

## Service description
{{ cookiecutter.project_description }}

## Terms of Reference
* TODO

## Technical solution
* TODO

## Interaction with 3rd party services
* TODO

## Scalability
Scalability is done by `Kubernetes` tools, by adding additional pods.
It is possible to scale by `gunicorn`, by adding additional workers.

## Dependency installation

```bash
$ poetry new {{ cookiecutter.project_name }}      // create a virtual environment
$ cd {{ cookiecutter.project_name }}
$ poetry shell              // activate the virtual environment for the current folder
```
Install the necessary packages:

```bash
({{ cookiecutter.project_name }})$ poetry install --no-dev      // install the main project dependencies
({{ cookiecutter.project_name }})$ poetry install       // install the main and dev dependencies of the project
```

**Important**: 
before running in a container, be sure to execute the ``poetry install'' command, 
command to generate poetry.lock - this is the file from which information about dependencies is to be taken when building the image. 
You must also add this file to the git index.

## Startup inside Docker

```bash
$ docker-compose up
```

## Run tests

```bash
$ python -m pytest -vvs
```


## Start the Flake code analyzer

```bash
$ python -m flake8 -v
```


## Set pre-commit hook

```bash
$ pre-commit install
```