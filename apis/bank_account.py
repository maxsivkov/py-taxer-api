from flask_restx import Namespace, Resource, Model, fields
import app
from .model import profile_model, user_accounts_model, user_account_model

ns = Namespace('accounts', description='Счета', path="/user/<int:userId>")

"""UserAccounts - счета"""

@ns.route('/accounts/page/<int:pageNumber>')
@ns.param('userId', 'Идентификатор профиля')
@ns.param('pageNumber', 'Номер страницы')
class UserAccounts(Resource):
    @ns.marshal_with(user_accounts_model)
    def get(self, userId:int, pageNumber:int):
        '''Возвращает зарегистрированные счета для профиля постранично'''
        return app.taxerApi.user_accounts(userId, pageNumber)

@ns.route('/accounts')
@ns.param('userId', 'Идентификатор профиля')
@ns.response(500, 'Shit happens')
class UserAccountsAll(Resource):
    @ns.marshal_list_with(user_account_model)
    def get(self, userId:int):
        '''Возвращает _все_ зарегистрированные счета для профиля'''
        return app.taxerApi.user_accounts_all(userId)

