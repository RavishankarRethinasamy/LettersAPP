import uuid
import logging
from datetime import datetime
from utils.db import insert_document, update_documents, find_documents, find_document
from common.definitions import Collections
from common.definitions import HttpCodes


class Blogs(object):

    def create(self, req_body):
        try:
            blog_dict = {
                "blog_id": str(uuid.uuid4()),
                "name": req_body["name"],
                "display_name": req_body["display_name"],
                "content": req_body["content"],
                "created_by": "admin",
                "created_at": datetime.utcnow(),
                "updated_by": "admin",
                "updated_at": datetime.utcnow(),
                "is_deleted": False
            }
            insert_document(Collections.BLOGS, blog_dict)
            return dict(status=HttpCodes.SUCCESS, message="Blog created successfully")
        except Exception as e:
            logging.error(str(e))
            raise Exception(str(e))

    def list(self, args):
        try:
            query = {
                "is_deleted": False
            }
            data = find_documents(Collections.BLOGS, query)
            count = data.count()
            page = args.get("page", 1)
            limit = args.get("limit", 15)
            paginated_data = find_documents(
                Collections.BLOGS, query, limit=limit, sort_fields=["created_by"])
            response_data = []
            for data in paginated_data:
                response_data.append({
                    "blog_id": data.get("blog_id"),
                    "name": data.get("name"),
                    "display_name": data.get("display_name"),
                    "description": data.get("description"),
                    "updates": {
                        "likes": data.get("updates", {}).get("likes", 0),
                        "dislikes": data.get("updates", {}).get("dislikes", 0)
                    }
                })
            response = {
                "data": response_data,
                "total": count,
                "page": page,
                "count": limit
            }
            return response
        except Exception as e:
            logging.error(str(e))
            raise Exception(str(e))

    def read(self, args):
        try:
            blog_id = args.get("blog_id")
            if not blog_id:
                raise Exception("blog Id is mandatory to get details")
            query = {
                "is_deleted": False,
                "blog_id": blog_id
            }
            blog_data = find_document(Collections.BLOGS, query)
            if not blog_data:
                raise Exception("Unable to find the blog details")
            latest_blogs = find_documents(Collections.BLOGS, {}, sort_fields=["created_at"], descending=True, limit=3)
            popular_blogs  = find_documents(Collections.BLOGS, {}, sort_fields=["updated.likes"], descending=True, limit=3)
            latest_content, popular_content = [], []
            for lb in latest_blogs:
                latest_content.append({
                    "display_name": lb["display_name"],
                    "blog_id": lb["blog_id"]
                })
            for pb in popular_blogs:
                popular_content.append({
                    "display_name": lb["display_name"],
                    "blog_id": lb["blog_id"]
                })
            updates = blog_data["updates"]
            updates["comments_count"] = len(updates.get("comments", []))
            response = {
                "data": blog_data["content"],
                "updated": updates,
                "latest_contents": latest_content,
                "popular_contents": popular_content
            }
            return response
        except Exception as e:
            logging.error(str(e))
            raise Exception(str(e))

    def update(self, req_body):
        try:
            blog_id = req_body.get("blog_id")
            type = req_body.get("type")
            if not blog_id:
                raise Exception("blog Id is mandatory to update details")
            query = {
                "is_deleted": False,
                "blog_id": blog_id
            }
            if type == "like":
                update_documents(Collections.BLOGS, query, {
                    "$inc": {
                        "updates.likes": 1
                    }
                })
            if type == "dislike":
                update_documents(Collections.BLOGS, query, {
                    "$inc": {
                        "updates.dislikes": 1
                    }
                })
            if type == "comment":
                comment = req_body.get("comment", "")
                update_documents(Collections.BLOGS, query, {
                    "$push": {
                        "updates.comments": comment
                    }
                })
            return {}
        except Exception as e:
            logging.error(str(e))
            raise Exception(str(e))
