from typing import List
import marshmallow_dataclass
from flask_restx import Namespace, Resource, Model, fields
from flask import request
import app
from .model import *
from .lucene_filter import Lucene2Filter
from taxer_model import OperationBrief, OperationsBrief, OperationDetail

ns = Namespace('operation', description='Операции', path="/user/<int:userId>")

def oper2resource(op:str):
    s = op.lower()
    if s == 'withdrawal':
        return WithdrawalOperation
    if s == 'flowoutgo':
        return FlowOutgoOperation
    if s == 'flowincome':
        return FlowIncomeOperation
    if s == 'currencyexchange':
        return CurrencyExchangeOperation
    if s == 'autoexchange':
        return AutoExchangeOperation
    raise Exception("Operation {} not known".format(op))

class Lucene2OperationFilter(Lucene2Filter):
    def special(self, tree, name:str, low_value:str, high_value:str) -> Dict[str, object]:
        result = {}
        if name == 'filterDate':
            result = {name: {'dateFrom': self.dt2timestamp_low(low_value),
                             'dateTo': self.dt2timestamp_high(high_value)}}
        if name == 'filterTotal':
            expr = None
            if tree.expr.include_low and tree.expr.include_high and low_value == high_value:
                expr = f'equal-{low_value}'
            elif low_value != '*':
                expr = f'more-{low_value}'
            elif high_value != '*':
                expr = f'less-{high_value}'
            result = {name: expr}
        return result
def operation_filter(q): return Lucene2OperationFilter(q).filter() if q is not None and len(q) > 0 else {}

"""Operations brief"""

@ns.route('/operation')
@ns.param('userId', 'Идентификатор профиля')
@ns.param('q', 'строка поиска в Lucene нотации')
class OperationsAll(Resource):
    @ns.marshal_list_with(operation_brief_model)
    def get(self, userId: int):
        '''Возвращает краткое описание _всех_ операций. Может занять определенное время'''
        ops:List[OperationBrief] = app.taxerApi.operations_all(userId, operation_filter(request.args.get('q', None, str)))
        for op in ops:
            op.path = self.api.url_for(oper2resource(op.type), userId=userId, operationId=op.id) #_external=True,
        return ops

@ns.route('/operation/page/<int:pageNumber>')
@ns.param('userId', 'Идентификатор профиля')
@ns.param('pageNumber', 'Номер страницы')
@ns.param('q', 'строка поиска в Lucene нотации')
class OperationsBrief(Resource):
    @ns.marshal_with(operations_brief_model)
    def get(self, userId:int, pageNumber:int):
        '''Возвращает краткое описание операций постранично'''
        ops:OperationsBrief = app.taxerApi.operations(userId, pageNumber, operation_filter(request.args.get('q', None, str)))
        for op in ops.operations:
            op.path = self.api.url_for(oper2resource(op.type), userId=userId, operationId=op.id) #_external=True,
        return ops

"""Withdrawal - Перевод между счетами"""

@ns.route('/operation/withdrawal/<int:operationId>')
@ns.param('userId', 'Идентификатор профиля')
@ns.param('operationId', 'Идентификатор операции')
class WithdrawalOperation(Resource):
    @ns.marshal_with(operation_withdrawal_model)
    def get(self, userId: int, operationId: int):
        '''Возвращает _полные_ данные по "Переводу между счетами"'''
        return app.taxerApi.operation_detail(userId, operationId, 'Withdrawal')
@ns.route('/operation/withdrawal')
@ns.param('userId', 'Идентификатор профиля')
class AddWithdrawalOperation(Resource):
    @ns.expect(add_operation_withdrawal_model, validate=True)
    @ns.marshal_with(add_operation_response_model)
    def post(self, userId:int):
        '''Перевод между счетами'''
        print('api.payload', self.api.payload)
        setop_schema = marshmallow_dataclass.class_schema(OperationDetail)
        op:OperationDetail = setop_schema().load(self.api.payload)
        op.type = 'Withdrawal'
        return app.taxerApi.add_operation(userId, op)


"""FlowOutgo - Расход"""

@ns.route('/operation/flowoutgo/<int:operationId>')
@ns.param('userId', 'Идентификатор профиля')
@ns.param('operationId', 'Идентификатор операции')
class FlowOutgoOperation(Resource):
    @ns.marshal_with(operation_flowoutgo_model)
    def get(self, userId: int, operationId: int):
        '''Возвращает _полные_ данные по "Расходу"'''
        return app.taxerApi.operation_detail(userId, operationId, 'FlowOutgo')
@ns.route('/operation/flowoutgo')
@ns.param('userId', 'Идентификатор профиля')
class AddFlowOutgoOperation(Resource):
    @ns.expect(add_operation_flowoutgo_model, validate=True)
    @ns.marshal_with(add_operation_response_model)
    def post(self, userId: int):
        '''Добавление Расход-а'''
        print('api.payload', self.api.payload)
        setop_schema = marshmallow_dataclass.class_schema(OperationDetail)
        op: OperationDetail = setop_schema().load(self.api.payload)
        op.type = 'FlowOutgo'
        return app.taxerApi.add_operation(userId, op)

"""FlowIncome - Доход"""

@ns.route('/operation/flowincome/<int:operationId>')
@ns.param('userId', 'Идентификатор профиля')
@ns.param('operationId', 'Идентификатор операции')
class FlowIncomeOperation(Resource):
    @ns.marshal_with(operation_flowincome_model)
    def get(self, userId: int, operationId: int):
        '''Возвращает _полные_ данные по "Доходу"'''
        return app.taxerApi.operation_detail(userId, operationId, 'FlowIncome')

@ns.route('/operation/flowincome')
@ns.param('userId', 'Идентификатор профиля')
class AddFlowIncomeOperation(Resource):
    @ns.expect(add_operation_flowincome_model, validate=True)
    @ns.marshal_with(add_operation_response_model)
    def post(self, userId: int):
        '''Добавление Доход-а'''
        print('api.payload', self.api.payload)
        setop_schema = marshmallow_dataclass.class_schema(OperationDetail)
        op: OperationDetail = setop_schema().load(self.api.payload)
        op.type = 'FlowIncome'
        if None == op.financeType:
            op.financeType = 'custom'
        return app.taxerApi.add_operation(userId, op)

"""CurrencyExchange - Обмен Валюты"""

@ns.route('/operation/currencyexchange/<int:operationId>')
@ns.param('userId', 'Идентификатор профиля')
@ns.param('operationId', 'Идентификатор операции')
class CurrencyExchangeOperation(Resource):
    @ns.marshal_with(currency_exchange_model)
    def get(self, userId: int, operationId: int):
        '''Возвращает _полные_ данные по Обмену Валюты'''
        op:OperationDetail = app.taxerApi.operation_detail(userId, operationId, 'CurrencyExchange')
        if None != op.exchangeDifference and None != op.exchangeDifference.total:
            op.exchangeDifferenceAmount = op.exchangeDifference.total
        op.total = op.outgoTotal * op.incomeCurrency
        return op

@ns.route('/operation/currencyexchange')
@ns.param('userId', 'Идентификатор профиля')
class AddCurrencyExchangeOperation(Resource):
    @ns.expect(add_currency_exchange_model, validate=True)
    @ns.marshal_with(add_operation_response_model)
    def post(self, userId: int):
        '''Добавление Обмена Валюты'''
        print('api.payload', self.api.payload)
        setop_schema = marshmallow_dataclass.class_schema(OperationDetail)
        op: OperationDetail = setop_schema().load(self.api.payload)
        op.type = 'CurrencyExchange'
        op.financeType = 'custom'
        return app.taxerApi.add_operation(userId, op)


"""AutoExchange - Валютный доход"""

@ns.route('/operation/autoexchange/<int:operationId>')
@ns.param('userId', 'Идентификатор профиля')
@ns.param('operationId', 'Идентификатор операции')
class AutoExchangeOperation(Resource):
    @ns.marshal_with(auto_exchange_model)
    def get(self, userId: int, operationId: int):
        '''Возвращает _полные_ данные по Валютному доходу'''
        return app.taxerApi.operation_detail(userId, operationId, 'AutoExchange')

@ns.route('/operation/autoexchange')
@ns.param('userId', 'Идентификатор профиля')
class AddAutoExchangeOperation(Resource):
    @ns.expect(add_auto_exchange_model, validate=True)
    @ns.marshal_with(add_operation_response_model)
    def post(self, userId: int):
        '''Добавление Валютномго дохода'''
        print('api.payload', self.api.payload)
        setop_schema = marshmallow_dataclass.class_schema(OperationDetail)
        op: OperationDetail = setop_schema().load(self.api.payload)
        op.type = 'AutoExchange'
        op.financeType = 'custom'
        return app.taxerApi.add_operation(userId, op)
