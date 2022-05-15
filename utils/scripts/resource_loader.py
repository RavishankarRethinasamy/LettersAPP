import os
import sys
import json
import argparse

possible_topdir = os.path.normpath(os.path.join(
    os.path.abspath(os.path.join(sys.argv[0], os.pardir, os.pardir))))

if os.path.exists(os.path.join(possible_topdir, 'app', '../__init__.py')):
    sys.path.insert(0, possible_topdir)

from utils.db import update_documents
from common.definitions import Collections

JSON_MASTER_PATH = "/utils/json"

json_file_to_load = [
    "category.json"
]

parser = argparse.ArgumentParser()
parser.add_argument("--inputs")
args = parser.parse_args()


def load_category(content):
    for value in content:
        update_documents(Collections.CATEGORY, {
            "name": value
        }, {
                             "$set": {
                                 "name": value
                             }
                         }, upsert=True)
    print("Loading Category collection is completed")


def main():
    to_load = args.inputs.split(",")
    for t in to_load:
        if t == "json":
            for ftol in json_file_to_load:
                with open(JSON_MASTER_PATH + ftol, "r") as fr:
                    content = fr.read()
                    if ftol.split(".")[0] == "category":
                        load_category(json.loads(content))


if __name__ == "__main__":
    main()
