import json
import os
import sys
from oslo_config import cfg

possible_topdir = os.path.normpath(os.path.join(os.path.abspath(os.path.join(sys.argv[0], os.pardir, os.pardir,
                                                                             os.pardir))))

if os.path.exists(os.path.join(possible_topdir, 'app', '__init__.py')):
    sys.path.insert(0, possible_topdir)

from app.api.v1.blog.actions import Blogs
from common import config

resource_path = "/opt/core/Letters/resources/test"


def load_resource(content_path):
    with open(content_path, "r") as cr:
        content = json.loads(cr.read())
    Blogs().create(content)


def main():
    for content_dir in os.listdir(resource_path):
        resource_path_dir = resource_path + f"/{content_dir}"
        for resource_content_file in os.listdir(resource_path_dir):
            if resource_content_file.endswith(".json"):
                content_path = resource_path_dir + f"/{resource_content_file}"
                try:
                    load_resource(content_path)
                except Exception as e:
                    print(str(e))
                    print(f"Error occurred while loading :: {resource_path_dir}")
                    continue
                print(f"Loading Completed :: {resource_path_dir}")


if __name__ == "__main__":
    cfg.CONF(project='letters', prog='letters-api')
    config.sanity_check()
    main()

