import uuid
import logging
import traceback
from datetime import datetime
from string import punctuation
from utils.db import insert_document, update_documents, find_documents, \
    aggregate_collection, remove_documents, get_count
from common.definitions import Collections
from common.utils import pagination


class Blogs(object):

    def create_description(self, contents):
        desc = ""
        for content in contents:
            if isinstance(content["insert"], str):
                if content["insert"] == "\n":
                    continue
                desc += content["insert"].replace("\n", " ")
                if len(desc) > 302:
                    break
        return f'{desc}...' if len(desc) < 302 else f'{desc[0:301]}...'

    def generate_blog_id(self, name):
        for sc in punctuation:
            if sc in name:
                name = name.replace(sc, '-')
        id_string = name.replace(" ", "-")
        return f'{id_string}-{str(uuid.uuid4())}'

    def create(self, req_body, kwargs):
        try:
            blog_dict = {
                "blog_id": self.generate_blog_id(req_body["name"]),
                "name": req_body["name"],
                "display_name": req_body["name"],
                "description": self.create_description(req_body["content"]),
                "content": req_body["content"],
                "created_by": kwargs.get("user_name", "guest"),
                "created_at": datetime.utcnow(),
                "is_deleted": False,
                "is_public": req_body.get("is_public", True),
                "type": req_body.get("type", "story"),
                "category": req_body.get("category", [])
            }
            insert_document(Collections.BLOGS, blog_dict)
            insert_document(Collections.UPDATES, {
                "blog_id": blog_dict["blog_id"],
                "pays": 0,
                "comments": []
            })
            return dict(
                status="success",
                message="letter created successfully",
                blog_id=blog_dict["blog_id"])
        except Exception as e:
            logging.error(traceback.format_exc())
            return {
                "status": "error",
                "message": str(e)
            }

    def list(self, args, kwargs):
        try:
            count = get_count(Collections.BLOGS)
            page = int(args.get("page", 1))
            limit = int(args.get("limit", 10))
            skip_val = 0
            page_count = 1
            skip_val, limit, page_count = pagination(limit, page, count, page_count, skip_val)
            aggregate_query = [
                {
                    "$match": {
                        "is_deleted": False,
                        "is_public": True
                    }
                },
                {
                    "$lookup": {
                        "from": "updates",
                        "localField": "blog_id",
                        "foreignField": "blog_id",
                        "as": "updates"
                    }
                },
                {
                    "$unwind": "$updates"
                },
                {
                    "$sort": {
                        "created_at": -1
                    }
                },
                {
                    "$skip": skip_val
                },
                {
                    "$limit": limit
                },
                {
                    "$project": {
                        "blog_id": "$blog_id",
                        "name": "$name",
                        "display_name": "$display_name",
                        "description": "$description",
                        "created_by": "$created_by",
                        "created_at": {"$dateToString": {
                            "date": "$created_at",
                            "format": "%Y-%m-%d %H:%M:%S GMT",
                            "timezone": "GMT",
                        }},
                        "type": "$type",
                        "category": "$category",
                        "pays": "$updates.pays",
                        "_id": 0
                    }
                }
            ]
            if kwargs:
                aggregate_query[0]["$match"].update({
                    "created_by": kwargs["user_name"]
                })
            if args.get("search"):
                search_query = {
                    "display_name": {"$regex": args["search"], "$options": "i"}
                }
                search = args.get("search").split(" ")
                for s in search:
                    search_query.update(
                        {
                            "display_name": {"$regex": s, "$options": "i"}
                        }
                    )
                aggregate_query[0]["$match"].update(search_query)
            data = aggregate_collection(Collections.BLOGS, aggregate_query)
            return {
                "status": "success",
                "data": data,
                "total": count,
                "page": page_count
            }
        except Exception as e:
            logging.error(traceback.format_exc())
            return {
                "status": "error",
                "message": str(e)
            }

    def read(self, args):
        try:
            blog_id = args.get("blog_id")
            aggregate_query = [
                {
                    "$match": {
                        "blog_id": blog_id,
                        "is_deleted": False,
                        "is_public": True
                    }
                },
                {
                    "$lookup": {
                        "from": "updates",
                        "localField": "blog_id",
                        "foreignField": "blog_id",
                        "as": "updates"
                    }
                },
                {
                    "$unwind": "$updates"
                },
                {
                    "$project": {
                        "display_name": "$display_name",
                        "data": "$content",
                        "created_by": "$created_by",
                        "created_at": {"$dateToString": {
                            "date": "$created_at",
                            "format": "%Y-%m-%d %H:%M:%S GMT",
                            "timezone": "GMT",
                        }},
                        "type": "$type",
                        "category": "$category",
                        "updates": "$updates",
                        "_id": 0
                    }
                }
            ]
            if not blog_id:
                raise Exception("blog Id is mandatory to get details")
            data = aggregate_collection(Collections.BLOGS, aggregate_query)
            if not data:
                raise Exception("Unable to find the blog details")
            data = data[0]
            related_blogs = find_documents(Collections.BLOGS, {
                "display_name": {"$regex": data["display_name"], "$options": "i"}
            }, limit=5)
            related_contents = []
            for lb in related_blogs:
                if lb["blog_id"] == blog_id:
                    continue
                related_contents.append({
                    "display_name": lb["display_name"],
                    "blog_id": lb["blog_id"]
                })
            data["related_contents"] = related_contents
            data["updates"].pop("_id", "")
            return {
                "status": "success",
                "data": data
            }
        except Exception as e:
            logging.error(traceback.format_exc())
            return {
                "status": "error",
                "message": str(e)
            }

    def update(self, req_body, kwargs):
        try:
            blog_id = req_body.get("blog_id")
            type = req_body.get("type")
            if not blog_id:
                raise Exception("blog Id is mandatory to update details")
            query = {
                "blog_id": blog_id
            }
            if type == "pay":
                update_documents(Collections.UPDATES, query, {
                    "$inc": {
                        "pays": 1
                    }
                })
            elif type == "comment":
                update_documents(Collections.UPDATES, query, {
                    "$push": {
                        "comments": {
                            "id": str(uuid.uuid4()),
                            "user": kwargs.get("user_name", "guest"),
                            "created_at": datetime.utcnow(),
                            "data": req_body["comment"]
                        }
                    }
                })
            elif type == "comment_reply":
                update_documents(Collections.COMMENT_UPDATES, query, {
                    "$push": {
                        "comments": {
                            "id": str(uuid.uuid4()),
                            "user": kwargs.get("user_name", "guest"),
                            "created_at": datetime.utcnow(),
                            "data": req_body["comment"]
                        }
                    }
                })
            return {
                "status": "success",
                "message": "letter updated successfully"
            }
        except Exception as e:
            logging.error(traceback.format_exc())
            return {
                "status": "error",
                "message": str(e)
            }

    def delete(self, req_body, kwargs):
        try:
            delete_query = {
                "created_by": kwargs["user_name"]
            }
            if req_body and "blog_id" in req_body:
                delete_query["blog_id"] = req_body["blog_id"]
            records_to_delete = find_documents(Collections.BLOGS, delete_query)
            deletable_blog_ids = [b_id["blog_id"] for b_id in records_to_delete]
            remove_documents(Collections.UPDATES, {
                "blog_id": {
                    "$in": deletable_blog_ids
                }
            })
            remove_documents(Collections.BLOGS, {
                "blog_id": {
                    "$in": deletable_blog_ids
                }
            })
            return {
                "status": "success",
                "message": "letter deleted successfully"
            }
        except Exception as e:
            logging.error(traceback.format_exc())
            return {
                "status": "error",
                "message": str(e)
            }
