from bridgebeam import app
from bottle import request, static_file, template
import json
import logging

log = logging.getLogger('bridgebeam')

@app.route('/', method='GET')
def home_page():
    return template('home_page')

@app.route('/<type:re:(css|js|img)>/<file:path>', method='GET')
def get_static(type, file):
    return static_file(file, root='bridgebeam/static/{}/'.format(type)) 
