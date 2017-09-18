from flask import jsonify
from . import api
from app.exceptions import ValidationError

def bad_request(message):
    respose = jsonify({'error':'bad request','message':message})
    respose.status_code = 400
    return respose

def unauthorized(message):
    respose = jsonify({'error':'unauthorized','message':message})
    respose.status_code = 401

def forbidden(message):
    respose = jsonify({'error':'forbidden','message':message})
    respose.status_code = 403

@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])
