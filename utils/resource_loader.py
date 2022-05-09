import json
from utils.db import update_documents
from common.definitions import Collections

MASTER_PATH = "/opt/core/LettersAPP/utils/"

json_file_to_load = [
    "category.json"
]


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
    for ftol in json_file_to_load:
        with open(MASTER_PATH + ftol, "r") as fr:
            content = fr.read()
            if ftol.split(".")[0] == "category":
                load_category(json.loads(content))


if __name__ == "__main__":
    main()
