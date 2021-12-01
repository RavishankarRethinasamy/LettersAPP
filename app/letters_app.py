from flask import Flask
from flask_restful import Api
from app.api.v1.blog.route import BlogsRoute


app = Flask("letters")

api = Api(app)

api.add_resource(BlogsRoute, "/fcs/letters/v1/blog/<action_name>")


