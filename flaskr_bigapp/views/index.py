from flask import Blueprint, render_template, request
from flask_restful import Api, Resource

index = Blueprint('index',__name__)
index_api = Api(index)
#@index.route('/')
class Index(Resource):
    def get(self):
        return 'First APP!'
    def put(self):
        MESS = request.form['data']
        return MESS
index_api.add_resource(Index, '/')

