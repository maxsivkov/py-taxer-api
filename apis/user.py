from typing import List
import marshmallow_dataclass
from flask_restx import Namespace, Resource, Model, fields
import app
from .model import user_accounts_model, user_account_model, document_model_brief, documents_model,add_document_response_model
from taxer_model import UserDocuments, Document
ns = Namespace('document', description='Банковские счета и документы', path="/user/<int:userId>")

"""Documents - документы/контракты"""
def doc2resource(op:str):
    s = op.lower()
    if s == 'contract':
        return UserDocumentContract
    if s == 'act':
        return UserDocumentAct
    raise Exception("Document {} not known".format(op))

@ns.route('/documents/page/<int:pageNumber>')
@ns.param('userId', 'Идентификатор профиля')
@ns.param('pageNumber', 'Номер страницы')
class UserDocumentsPage(Resource):
    @ns.marshal_with(documents_model)
    def get(self, userId:int, pageNumber:int):
        '''Возвращает документы для профиля постранично'''
        docs:UserDocuments = app.taxerApi.documents(userId, pageNumber)

        for doc in docs.documents:
            doc.path = self.api.url_for(doc2resource(doc.type), userId=userId, docId=doc.id)  # _external=True,
        return docs

@ns.route('/documents')
@ns.param('userId', 'Идентификатор профиля')
@ns.response(500, 'Shit happens')
class UserDocumentsAll(Resource):
    @ns.marshal_list_with(document_model_brief)
    def get(self, userId:int):
        '''Возвращает _все_ документы для профиля'''
        docs: List[Document] = app.taxerApi.documents_all(userId)
        for doc in docs:
            doc.path = self.api.url_for(doc2resource(doc.type), userId=userId, docId=doc.id)  # _external=True,
        return docs

@ns.route('/document/contract/<int:docId>')
@ns.param('userId', 'Идентификатор профиля')
@ns.param('docId', 'Идентификатор документа')
@ns.response(500, 'Shit happens')
class UserDocumentContract(Resource):
    @ns.marshal_with(document_model_brief)
    def get(self, userId:int, docId:int):
        '''Возвращает расширенные свойства контракта для профиля'''
        return app.taxerApi.document(userId, docId, 'contract')
@ns.route('/document/contract')
@ns.param('userId', 'Идентификатор профиля')
class AddUserDocumentContract(Resource):
    @ns.expect(document_model_brief, validate=True)
    @ns.marshal_with(add_document_response_model)
    def post(self, userId:int):
        '''Перевод между счетами'''
        print('api.payload', self.api.payload)
        #setop_schema = marshmallow_dataclass.class_schema(SetOperation)
        #op:SetOperation = setop_schema().load(self.api.payload)
        #op.id = None
        #op.type = 'contract'
        #return app_taxer_api.taxerApi.add_operation(userId, op)


@ns.route('/document/act/<int:docId>')
@ns.param('userId', 'Идентификатор профиля')
@ns.param('docId', 'Идентификатор документа')
@ns.response(500, 'Shit happens')
class UserDocumentAct(Resource):
    @ns.marshal_with(document_model_brief)
    def get(self, userId:int, docId:int):
        '''Возвращает расширенные свойства акта для профиля'''
        return app.taxerApi.document(userId, docId, 'act')

"""TODO: Implement other document types: 'act'... """

