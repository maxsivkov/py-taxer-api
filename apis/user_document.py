import marshmallow_dataclass
from flask_restx import Namespace, Resource, Model, fields
import app
from .model import *
from taxer_model import UserDocuments, Document
ns = Namespace('document', description='Документы', path="/user/<int:userId>")

"""Documents - документы/контракты"""
def doc2resource(op:str):
    s = op.lower()
    if s == 'contract':
        return UserDocumentContract
    if s == 'act':
        return UserDocumentAct
    if s == 'invoice':
        return UserDocumentInvoice

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
    @ns.marshal_list_with(document_brief_model)
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
    @ns.marshal_with(document_contract_model)
    def get(self, userId:int, docId:int):
        '''Возвращает расширенные свойства контракта для профиля'''
        return app.taxerApi.document(userId, docId, 'contract')

@ns.route('/document/invoice/<int:docId>')
@ns.param('userId', 'Идентификатор профиля')
@ns.param('docId', 'Идентификатор документа')
@ns.response(500, 'Shit happens')
class UserDocumentInvoice(Resource):
    @ns.marshal_with(document_invoice_model)
    def get(self, userId:int, docId:int):
        '''Возвращает расширенные свойства инвойса для профиля'''
        return app.taxerApi.document(userId, docId, 'invoice')


@ns.route('/document/contract')
@ns.param('userId', 'Идентификатор профиля')
class UserDocumentContractList(Resource):
    @ns.expect(add_document_contract_model, validate=True)
    @ns.marshal_with(add_document_response_model)
    def post(self, userId:int):
        '''Добавление документа типа Договор'''
        #print('api.payload', self.api.payload)
        schema = marshmallow_dataclass.class_schema(Document)
        doc:Document = schema().load(self.api.payload)
        doc.type = 'contract'
        doc.file = {}
        return app.taxerApi.add_document(userId, doc)


@ns.route('/document/act/<int:docId>')
@ns.param('userId', 'Идентификатор профиля')
@ns.param('docId', 'Идентификатор документа')
@ns.response(500, 'Shit happens')
class UserDocumentAct(Resource):
    @ns.marshal_with(document_act_model)
    def get(self, userId:int, docId:int):
        '''Возвращает расширенные свойства акта для профиля'''
        return app.taxerApi.document(userId, docId, 'act')
@ns.route('/document/act')
@ns.param('userId', 'Идентификатор профиля')
class UserDocumentActList(Resource):
    @ns.expect(add_document_act_model, validate=True)
    @ns.marshal_with(add_document_response_model)
    def post(self, userId:int):
        '''Добавление документа типа Акт'''
        #print('api.payload', self.api.payload)
        schema = marshmallow_dataclass.class_schema(Document)
        doc:Document = schema().load(self.api.payload)
        doc.type = 'act'
        doc.file = {}
        if doc.contents is None:
            doc.contents = []
        return app.taxerApi.add_document(userId, doc)


"""TODO: Implement other document types: 'act'... """

