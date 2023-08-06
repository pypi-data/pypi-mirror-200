import os
import argparse

from sonotoria import jaml

from .project import create_full_project


def main():
    parser = argparse.ArgumentParser(description='Initiate a project on Gitlab.')
    parser.add_argument('conf_path', type=str, help='The config file')
    parser.add_argument('--token', dest='token', type=str, help='The gitlab token')

    args = parser.parse_args()

    conf = jaml.load(args.conf_path)
    conf['token'] = args.token or os.environ['GL_TOKEN']
    create_full_project(conf)


if __name__ == '__main__':
    main()
