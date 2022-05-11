from app.api.v1.blog.actions import Blogs
from flask import request
from flask_restful import Resource

from utils.auth import authorize


class BlogsRoute(Resource):
    def __init__(self):
        self.actions = Blogs()

    @authorize
    def get(self, action_name=None, **kwargs):
        response = {}
        if action_name == "list":
            response = self.actions.list(request.args, kwargs)
        elif action_name == "read":
            response = self.actions.read(request.args)
        return response

    @authorize
    def post(self, action_name=None, **kwargs):
        response = {}
        if action_name == "create":
            response = self.actions.create(request.get_json(), kwargs)
        return response

    @authorize
    def put(self, action_name=None, **kwargs):
        response = {}
        if action_name == "update":
            response = self.actions.update(request.get_json(), kwargs)
        return response

    @authorize
    def delete(self, action_name=None, **kwargs):
        response = {}
        if action_name == "delete":
            response = self.actions.delete(request.get_json(), kwargs)
        return response
