from helloworld import app
from flask import Blueprint
test = Blueprint('hellworld',__name__)

@test.route('/index')
def index():
    return "Hello, World!"

@test.route('/mail')
def mail():
    return app.config.get('TEST1')