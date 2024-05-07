import os
import shutil

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def remove_directory(directory):
    shutil.rmtree(os.path.join(PROJECT_DIRECTORY, directory))


def make_directory(directory):
    os.mkdir(os.path.join(PROJECT_DIRECTORY, directory))


def copy_directory(directory, destination):
    shutil.copytree(directory, destination)


project_slug = '{{ cookiecutter.project_slug }}'
use_postgresql = '{{ cookiecutter.use_postgresql }}'.lower()
use_alembic = '{{ cookiecutter.use_alembic }}'.lower()

if __name__ == '__main__':
    if use_alembic != 'y':
        remove_file('alembic.ini')
        remove_directory(f'src/data/postgres/migrations')

    if use_postgresql != 'y':
        remove_directory(f'src/data')
        remove_file(f'src/api/items.py')
        remove_directory(f'src/use_cases/items')
        remove_file('tests/expected_data.py')
        remove_file('tests/mock_data.py')
        remove_file('tests/test_items.py')
