from flask import Flask, Response
import os

app = Flask(__name__)

@app.route('/') #Returns the app name
def home():
    app_name = os.getenv('APP_NAME', 'airtasker')
    return Response(app_name, mimetype='text/plain')

@app.route('/healthcheck') #Returns a simple healthcheck response
def healthcheck():
    return Response('OK', mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080) 