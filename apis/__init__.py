from flask_restx import Api
from flask import Flask
from .model import models
from .account import ns as ns_account
from .bank_account import ns as ns_bank_account
from .user_document import ns as ns_user
from .user_operation import  ns as ns_operation

def create_application(config_filename:str = None) -> Flask:
    app:Flask = Flask(__name__)

    if config_filename is not None:
        app.config.from_pyfile(config_filename)

    app.config.SWAGGER_UI_REQUEST_DURATION = True
    #app.config['RESTX_JSON'] = {'ensure_ascii' : False}
    #app.config['JSON_AS_ASCII'] = False
    api:Api = Api(app, version='1.0', title='Taxer API', description='taxer.ua proxy API', doc='/docs')

    for m in models:
        api.add_model(m.name, m)

    api.add_namespace(ns_account)
    api.add_namespace(ns_bank_account)
    api.add_namespace(ns_user)
    api.add_namespace(ns_operation)
    return app
