from bridgebeam import application
from bottle import request, static_file, template
import json
import logging
import os

log = logging.getLogger('bridgebeam')

@application.route('/', method='GET')
def home_page():
    return template('home_page')

@application.route('/<type:re:(css|js|img)>/<file:path>', method='GET')
def get_static(type, file):
    base_path = application.config.path
    return static_file(file, root='{}/static/{}/'.format(base_path, type)) 
