import logging
import requests
import traceback

from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS

from app.api.v1.blog.route import BlogsRoute
from app.api.v1.blog.actions import Blogs

from common.utils import parse_req
from common.definitions import Collections
from utils.db import insert_document

app = Flask("letters")
CORS(app)

api = Api(app)


# ************************************Unauthorized global APIs*********************************

@app.route("/v1/blog/global_list")
def list_blogs():
    try:
        return Blogs().list(request.args, kwargs={})
    except Exception as e:
        logging.error(traceback.format_exc())
        raise Exception(e)


@app.route("/v1/blog/global_read")
def read_blogs():
    try:
        return Blogs().read(request.args)
    except Exception as e:
        raise Exception(e)


@app.route("/v1/blog/global_update", methods=["PUT"])
def update_blogs():
    req_body = parse_req(request.get_data())
    return Blogs().update(req_body, kwargs={})


@app.route("/v1/blog/global_create", methods=["POST"])
def create_blog():
    req_body = parse_req(request.get_data())
    return Blogs().create(req_body, kwargs={})


@app.route("/v1/blog/recaptcha", methods=["POST"])
def verify_recaptcha():
    try:
        req_body = parse_req(request.get_data())
        verify_url = f"https://www.google.com/recaptcha/api/siteverify?" \
                     f"secret={req_body['secret']}&response={req_body['response']}"
        response = requests.post(verify_url)
        if response.ok:
            response = response.json()
            if response["success"]:
                insert_document(Collections.RECAPTCHA, response)
                if response["score"] < 0.5:
                    raise Exception("bot")
            else:
                raise Exception(" ".join(response["error-codes"]))
        else:
            raise Exception("Error occurred in recaptcha verification")
        return {"status": "success"}
    except Exception as e:
        logging.error(traceback.format_exc())
        return {
            "status": "error",
            "message": str(e)
        }


# ******************************************** Authorized User APIs *************************************

api.add_resource(BlogsRoute, "/v1/blog/<action_name>")
