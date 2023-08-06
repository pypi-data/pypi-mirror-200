import os
import tempfile

from sonotoria import jinja


def populate_repo(project, group):
    with tempfile.TemporaryDirectory() as td:
        project_path = f'{td}/{project.config["name"]}'
        src_path = f'{td}/src'
        os.system(f'git clone https://gitlab.com/kaeraspace/{group.group.name}/{project.config["name"]}.git {project_path}') # nosec B605
        os.system(f'git clone {project.config["src"]} {src_path}') # nosec B605

        if len(project.project.branches.list()) > 0:
            print('No need to populate repo. Skipping.')
            return

        jinja.template_folder(
            src_path,
            project_path,
            context={
                **group.config.get('vars', {}),
                **project.config.get('vars', {}),
                'project': project.config
            }
        )

        os.system(' && '.join([ # nosec B605
            f'cd {project_path}',
            'git switch -c master', # FUCK U GITLAB YOU MOTHER FUCKING WOKE IDIOTS!
            'git add .',
            'git commit -m ":sparkles: Kaera Init"',
            'git push --set-upstream origin master'
        ]))
