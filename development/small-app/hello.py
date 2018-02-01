from flask import Flask
small = Flask(__name__)
@small.route('/')
def hello_world():
    return 'Fuck you!'

if __name__ == '__main__':
    small.run()