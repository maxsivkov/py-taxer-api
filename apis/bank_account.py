from typing import Dict
import marshmallow_dataclass
from flask_restx import Namespace, Resource
from flask import request
from .model import user_accounts_model, user_bank_account_model, add_user_bank_account_model, add_user_bank_account_response_model
from taxer_model import UserAccount
from .lucene_filter import Lucene2Filter
import app

ns = Namespace('accounts', description='Банковские счета', path="/user/<int:userId>")

class Lucene2AccountFilter(Lucene2Filter):
    def special(self, tree, name:str, low_value:str, high_value:str) -> Dict[str, object]:
        result = {}
        if name == 'filterBalance':
            expr = None
            if tree.expr.include_low and tree.expr.include_high and low_value == high_value:
                expr = f'equal-{low_value}'
            elif low_value != '*':
                expr = f'more-{low_value}'
            elif high_value != '*':
                expr = f'less-{high_value}'
            result = {name: expr}
        return result
def account_filter(q): return Lucene2AccountFilter(q).filter() if q is not None and len(q) > 0 else {}


"""UserAccounts - счета"""

@ns.route('/accounts/page/<int:pageNumber>')
@ns.param('userId', 'Идентификатор профиля')
@ns.param('pageNumber', 'Номер страницы')
@ns.param('q', 'строка поиска в Lucene нотации')
class UserAccounts(Resource):
    @ns.marshal_with(user_accounts_model, skip_none=True)
    def get(self, userId:int, pageNumber:int):
        '''Возвращает зарегистрированные счета для профиля постранично'''
        return app.taxerApi.user_accounts(userId, account_filter(request.args.get('q', None, str)), pageNumber)

@ns.route('/accounts')
@ns.param('userId', 'Идентификатор профиля')
@ns.response(500, 'Shit happens')
class UserAccountsAll(Resource):
    @ns.marshal_list_with(user_bank_account_model, skip_none=True)
    def get(self, userId:int):
        '''Возвращает _все_ зарегистрированные счета для профиля'''
        return app.taxerApi.user_accounts_all(userId, account_filter(request.args.get('q', None, str)))

    @ns.expect(add_user_bank_account_model, validate=True)
    @ns.marshal_with(add_user_bank_account_response_model)
    def post(self, userId: int):
        '''Добавление нового счета'''
        schema = marshmallow_dataclass.class_schema(UserAccount)
        acc:UserAccount = schema().load(self.api.payload)
        return app.taxerApi.add_user_account(userId, acc)
