from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS

from app.api.v1.blog.route import BlogsRoute
from app.api.v1.blog.actions import Blogs

from common.utils import parse_req

app = Flask("letters")
CORS(app)

api = Api(app)


# ************************************Unauthorized global APIs*********************************

@app.route("/fcs/letters/v1/blog/global_list")
def list_blogs():
    try:
        return Blogs().list(request.args, kwargs={})
    except Exception as e:
        raise Exception(e)


@app.route("/fcs/letters/v1/blog/global_read")
def read_blogs():
    try:
        return Blogs().read(request.args)
    except Exception as e:
        raise Exception(e)


@app.route("/fcs/letters/v1/blog/global_update", methods=["PUT"])
def update_blogs():
    req_body = parse_req(request.get_data())
    return Blogs().update(req_body, kwargs={})


@app.route("/fcs/letters/v1/blog/global_create", methods=["POST"])
def create_blog():
    req_body = parse_req(request.get_data())
    return Blogs().create(req_body, kwargs={})


# ******************************************** Authorized User APIs *************************************

api.add_resource(BlogsRoute, "/fcs/letters/v1/blog/<action_name>")
