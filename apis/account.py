from flask_restx import Namespace, Resource, Model, fields
import app
from .model import profile_model, user_accounts_model, user_account_model

ns = Namespace('account', description='Учетная запись')

@ns.route('')
class AccountApi(Resource):
    @ns.marshal_with(profile_model)
    def get(self):
        '''Возвращает учетную запись вместе с профилями предприятий/ФОПов '''
        return app.taxerApi.account()

