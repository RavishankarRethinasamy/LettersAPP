import time
import uuid
import logging
from datetime import datetime
from utils.db import insert_document, update_documents, find_documents, aggregate_collection
from common.definitions import Collections
from common.utils import pagination


class Blogs(object):

    def create(self, req_body, kwargs):
        try:
            blog_dict = {
                "blog_id": str(uuid.uuid4()),
                "name": req_body["name"],
                "display_name": req_body["name"],
                "content": req_body.get("content", []),
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
            time.sleep(1)
            return dict(
                status="success",
                message="letter created successfully",
                blog_id=blog_dict["blog_id"])
        except Exception as e:
            logging.error(str(e))
            raise Exception(str(e))

    def list(self, args, kwargs):
        try:
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
                    "$project": {
                        "blog_id": "$blog_id",
                        "name": "$name",
                        "display_name": "$display_name",
                        "created_by": "$created_by",
                        "created_at": "$created_at",
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
            # count = len(data)
            # page = int(args.get("page", 1))
            # limit = int(args.get("limit", 3))
            # skip_val = 0
            # page_count = 1
            # skip_val, limit, page_count = pagination(limit, page, count, page_count, skip_val)
            # data = data[skip_val:]
            # data = data[:limit]
            return {
                "status": "success",
                "data": data
            }
        except Exception as e:
            logging.error(str(e))
            raise Exception(str(e))

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
                        "created_at": "$created_at",
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
            return data
        except Exception as e:
            logging.error(str(e))
            raise Exception(str(e))

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
            if type == "comment":
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
            return {
                "status": "success",
                "message": "letter updated successfully"
            }
        except Exception as e:
            logging.error(str(e))
            raise Exception(str(e))

    def delete(self, req_body, kwargs):
        try:
            blog_id = req_body.get("blog_id")
            if not blog_id:
                raise Exception("blog Id is mandatory to update details")
            update_documents(Collections.BLOGS, {
                "blog_id": blog_id
            }, {
                                 "$set": {
                                     "is_deleted": True,
                                     "deleted_by": kwargs["user_name"]
                                 }
                             })
            return {
                "message": "letter deleted successfully"
            }
        except Exception as e:
            raise Exception(e)
