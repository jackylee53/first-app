# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g , jsonify
from flask_restful import reqparse

from . import Resource
from .. import schemas


class Cmdb(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user',type=str)
        parser.add_argument('test',type=str)
        args = parser.parse_args()
        user = args['user']
        test = args['test']
        return jsonify({'test':user,'test2':test})