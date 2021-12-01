from oslo_config import cfg
from pymongo import MongoClient


def connect(collection_name):
    connection_string = f"mongodb://{cfg.CONF.mongo_host}:{cfg.CONF.mongo_port}/"
    client = MongoClient(connection_string)
    db_conn = client[cfg.CONF.database_name]
    coll_conn = db_conn[collection_name]
    return coll_conn


def insert_document(collection_name, insert_data):
    conn = connect(collection_name)
    conn.insert_one(insert_data)


def update_document(collection_name, query, updated_data):
    conn = connect(collection_name)
    conn.update_one(query, updated_data)


def update_documents(collection_name, query, updated_data):
    conn = connect(collection_name)
    conn.update_many(query, updated_data)


def find_document(collection_name, query):
    conn = connect(collection_name)
    return conn.find_one(query)


def find_documents(collection_name, query, sort_fields=[], limit=0):
    conn = connect(collection_name)
    if sort_fields:
        pass
    if limit:
        pass
    data = conn.find(query)
    return list(data)


def remove_documents(collection_name, query):
    conn = connect(collection_name)
    conn.remove(query)
