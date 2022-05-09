from pymongo import MongoClient, cursor
from bson import ObjectId
from pymongo import ASCENDING
from pymongo import DESCENDING

from common.config import args


def connect(collection_name):
    connection_string = f"mongodb://{args.get('MAIN.mongo_host')}:{args.get('MAIN.mongo_port')}/"
    client = MongoClient(connection_string)
    db_conn = client["letters"]
    coll_conn = db_conn[collection_name]
    return coll_conn


def insert_document(collection_name, insert_data, fields=None):
    if not fields:
        fields = ["_id"]
    conn = connect(collection_name)
    insert_ids = conn.insert(insert_data)
    if isinstance(insert_ids, list):
        result = insert_ids
    else:
        result = conn.find_one({"_id": ObjectId(insert_ids)}, fields)
    return result


def update_documents(collection_name, query, updated_data, upsert=False, multi=True):
    conn = connect(collection_name)
    return conn.update(query, updated_data, upsert=upsert, multi=multi)


def find_document(collection_name, query):
    conn = connect(collection_name)
    return conn.find_one(query)


def find_documents(collection_name, query=None, sort_fields=[], descending=False,
                   limit=0, skip_val=0):
    if not query:
        query = dict()
    conn = connect(collection_name)
    sort_query = dict()
    if sort_fields:
        if descending:
            sort_query = [(field, DESCENDING) for field in sort_fields]
        else:
            sort_query = [(field, ASCENDING) for field in sort_fields]
    documents = conn.find(query)
    if sort_query:
        documents = documents.sort(sort_query)
    if limit:
        documents = documents.skip(skip_val).limit(limit)
    return list(documents)


def aggregate_collection(collection_name, query):
    conn = connect(collection_name)
    return list(conn.aggregate(query, cursor={}))


def get_distinct_fields(collection_name, field_name, query=None):
    conn = connect(collection_name)
    if query:
        result = conn.find(query).distinct(field_name)
    else:
        result = conn.distinct(field_name)
    return result


def remove_documents(collection_name, query):
    conn = connect(collection_name)
    conn.remove(query)
