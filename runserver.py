from flaskr_bigapp import create_app

app = create_app('conf/development.conf')
app.run(host='0.0.0.0')