import re
import sys

PROJECT_SLUG_RE = re.compile(r'^[_a-zA-Z][_a-zA-Z0-9]+$')
APP_NAME_RE = re.compile(r'^[a-zA-Z0-9-]+$')

project_slug = '{{ cookiecutter.project_slug }}'
use_postgresql = '{{ cookiecutter.use_postgresql }}'.lower()
use_alembic = '{{ cookiecutter.use_alembic }}'.lower()
use_kafka = '{{ cookiecutter.use_kafka }}'.lower()
use_redis = '{{ cookiecutter.use_redis }}'.lower()

if __name__ == '__main__':
    exit_code = 0

    if not PROJECT_SLUG_RE.match(project_slug):
        print(
            f'ERROR: The project slug {project_slug} is not a valid Python module name. '
            f'Please do not use a - and use _ instead'
        )

        exit_code = 1

    if use_alembic == 'y' and use_postgresql != 'y':
        print('ERROR: inconsistent configuration, you can\'t use alembic without gino')

        exit_code = 1

    sys.exit(exit_code)
