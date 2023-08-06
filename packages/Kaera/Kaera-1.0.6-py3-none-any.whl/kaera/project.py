from contextlib import contextmanager

from .population import populate_repo
from .gitlab_handler import GitlabHandler
from .default import LABELS, BOARDS


def create_full_project(config):
    handler = GitlabHandler(config['token'])

    with ensure(f'group {config["group"]["name"]} is present'):
        group = handler.create_group(config['group'])

    for project_config in config['projects']:
        with ensure(f'project {project_config["name"]} is present'):
            create_repo(project_config, group)


def create_repo(project_config, group):
    with ensure('repo is created'):
        project = group.create_project(project_config)

    with ensure('repo is populated'):
        populate_repo(project, group)

    with ensure('repo branches are protected'):
        project.protect_branches()

    with ensure('repo config is set'):
        project.set_config()

    if not project_config.get('skip_labels', False):
        with ensure('labels are present'):
            project.create_labels(project_config.get('labels', LABELS))
    else:
        other('Skipping labels...')

    if not project_config.get('skip_boards', False):
        with ensure('boards are present'):
            project.create_boards(project_config.get('boards', BOARDS))
    else:
        other('Skipping boards...')


@contextmanager
def ensure(str_):
    print(f'\u001b[33mEnsure {str_}...\u001b[39m')
    yield None
    print(f'\u001b[32mSuccessfully ensured {str_}!\u001b[39m\n')


def other(str_):
    print(f'\u001b[34m{str_}\u001b[39m')
