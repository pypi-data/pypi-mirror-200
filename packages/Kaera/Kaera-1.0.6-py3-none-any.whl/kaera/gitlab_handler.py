from gitlab import Gitlab
from gitlab.const import MAINTAINER_ACCESS


KAERASPACE_ID = 13844027


class _Project:
    def __init__(self, group, project, config):
        self.group = group
        self.project = project
        self.config = config
        self.labels = {}

    def protect_branches(self):
        if len(self.project.protectedbranches.list()) > 1:
            return
        self.project.protectedbranches.get('master').delete()
        self.project.protectedbranches.create({
            'name': 'master',
            'merge_access_level': MAINTAINER_ACCESS,
            'push_access_level': MAINTAINER_ACCESS,
            'allow_force_push': True
        })
        self.project.protectedbranches.create({
            'name': '*.*',
            'merge_access_level': MAINTAINER_ACCESS,
            'push_access_level': MAINTAINER_ACCESS,
            'allow_force_push': False
        })

    def create_labels(self, labels):
        self.labels = {
            name: self.create_label(name, color)
            for name, color in labels.items()
        }

    def create_boards(self, boards):
        for name, label_names in boards.items():
            self.create_board(name, self.labels, label_names)

    def create_label(self, name, color):
        label = find_by_name(self.project.labels.list(), name)
        if not label:
            return self.project.labels.create({'name': name, 'color': color})
        label.color = color
        label.save()
        return label

    def create_board(self, name, labels, label_names):
        board = find_by_name(self.project.boards.list(), name)
        if not board:
            board = self.project.boards.create({'name': name})
        for label_name in label_names:
            create_list(board, labels[label_name].id)

    def set_config(self):
        pass


class _Group: # pylint: disable=too-few-public-methods
    def __init__(self, group, gl, config):
        self.group = group
        self.gl = gl
        self.config = config

    def create_project(self, config):
        config['name'] = config['name'].lower()
        project = find_by_name(self.group.projects.list(all=True, owned=True), config['name'].capitalize())
        if project:
            project = self.gl.projects.get(project.attributes['id'])
        else:
            project = self.gl.projects.create({
                'name': config['name'].capitalize(),
                'namespace_id': self.group.id,
                'merge_method': 'ff'
            })
        update_resource(project, config.get('desc', ''), config.get('img', None))
        return _Project(self.group, project, config)


class GitlabHandler: # pylint: disable=too-few-public-methods
    def __init__(self, token):
        self.gl = Gitlab('https://gitlab.com', private_token=token)
        self.gl.auth()

    def create_group(self, config):
        group = find_by_name(self.gl.groups.list(owned=True), config['name'])
        if not group:
            group = self.gl.groups.create({
                'name': config['name'],
                'path': config['name'].replace(' ', ''),
                'parent_id': KAERASPACE_ID
            })
        update_resource(group, config.get('desc', ''), config.get('img', None))
        return _Group(group, self.gl, config)


def update_resource(resource, desc, img):
    resource.description = desc
    if img is not None:
        with open(img, 'rb') as img_file:
            resource.avatar = img_file
            resource.save()
            return
    resource.save()


def create_list(board, label_id):
    list_ = find(board.lists.list(), lambda lst: lst.label['id'] == label_id)
    if not list_:
        board.lists.create({'label_id': label_id})


def find_by_name(lst, name):
    return next((el for el in lst if el.name == name), None)


def find(lst, cond):
    return next((el for el in lst if cond(el)), None)


def fuck(project):
    main = project.branches.get('main')
    master = project.branches.create({'branch': 'master', 'ref': 'main'})
    main.unprotect()
    master.protect()
    main.delete()
