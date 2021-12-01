from app.api.v1.blog.actions import Blogs
from flask import request
from flask_restful import Resource


class BlogsRoute(Resource):
    def __init__(self):
        self.actions = Blogs()

    def get(self, action_name=None):
        if action_name == "list":
            response = self.actions.list(request.args)
        elif action_name == "read":
            response = self.actions.read(request.args)
        return response

    def post(self, action_name):
        if action_name == "create":
            response = self.actions.create(request.get_json())
        return response

    def put(self, action_name):
        if action_name == "update":
            response = self.actions.update(request.get_data(), request.args)
        return response
