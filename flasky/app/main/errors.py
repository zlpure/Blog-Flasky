from flask import  render_template,request,jsonify
from . import main

@main.app_errorhandler(403)
def forbidden(e):
    if request.accept_mimetypes.accept_json and \
        not request.accept_mimetypes.accept_html:
        respose = jsonify({'error':'forbidden'})
        respose.status_code=403
        return respose
    return render_template('403.html'),403

@main.app_errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and \
        not request.accept_mimetypes.accept_html:
        respose = jsonify({'error':'not found'})
        respose.status_code = 404
        return respose
    return render_template('404.html'),404

@main.app_errorhandler(500)
def internal_server_error(e):
    if request.accept_mimetypes.accept_json and \
        not request.accept_mimetypes.accept_html:
        respose = jsonify({'error':'internal server error'})
        respose.status_code = 500
        return respose
    return render_template('500.html'),500