import logging
import requests
import ujson
from collections import namedtuple
from taxer_model import *

from taxer_driver import TaxerDriverBase
import marshmallow_dataclass
from marshmallow.utils import EXCLUDE, INCLUDE


class TaxerApi:
    def __init__(self, taxer_driver:TaxerDriverBase):
        self.taxer_driver = taxer_driver
        self.logger = logging.getLogger(__name__)
        self.lang='uk'

    def execute(self, method, path, json=None):
        data = ujson.dumps(json, ensure_ascii=False).encode(encoding='utf-8') if json is not None else None
        self.logger.debug(f'------------------------------------------------------')
        self.logger.info(f'Req {method} {path}')
        if data is not None:
            self.logger.debug('json {}'.format(json))
            self.logger.debug('data {}'.format(data))
        headers = {'X-XSRF-TOKEN': self.taxer_driver.token,
                   'Origin': 'https://taxer.ua',
                   'Referer': 'https://taxer.ua/ru/my',
                   'Content-Type': 'application/json; charset=UTF-8',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
                   }
        response = requests.request(method, self.taxer_driver.get_url(path), cookies=self.taxer_driver.cookies, headers=headers, data=data)
        self.logger.debug('request {}'.format(response.request.url))
        self.logger.debug('request headers\n{}'.format('\n'.join([f'{k}: {v}' for k, v in response.request.headers.items()])))
        self.logger.debug('request body {}'.format(response.request.body))

        self.logger.debug('response status_code {}'.format(response.status_code))
        self.logger.debug('response headers\n{}'.format('\n'.join([f'{k}: {v}' for k, v in response.headers.items()])))
        self.logger.debug('response body {}'.format(response.content))
        self.logger.debug('response text {}'.format(response.text))
        self.logger.debug('response json {}'.format(response.json()))

        response.raise_for_status()

        return response.json()

    def all_pages(self, userId: int, get_content, extract_payload) -> List:
        """
        Retrieve all pages for an entiry. Entity must be pageable
        :param userId: user identifier
        :param get_content: function that returns next page with content
        :param extract_payload: extract payload (return list)
        :return:
        """
        pageNumber:int = 1
        done:bool = False
        result:List = []
        while not done:
            paged_content = get_content(userId, pageNumber)
            result.extend(extract_payload(paged_content))
            pageNumber = paged_content.paginator.currentPage + 1
            done = paged_content.paginator.currentPage >= paged_content.paginator.totalPages
        return result

    def account(self) -> Account:
        json = self.execute('POST', 'api/user/login/load_account?lang={}'.format(self.lang))
        schema = marshmallow_dataclass.class_schema(Account)
        return schema().load(json['content']['account'])

    def operations(self, userId:int, pageNumber:int = 1) -> OperationsBrief:
        self.logger.debug('operations @ {} [pg {}] ->'.format(userId, pageNumber))
        json = self.execute('POST', 'api/finances/operation/load?lang={}'.format(self.lang), json={
            'userId': userId,
            'pageNumber': pageNumber,
            'filters': {}
        })
        schema = marshmallow_dataclass.class_schema(OperationsBrief)
        #result:Operations = schema(exclude=['operations.contents.date']).load(json, partial=True, unknown=EXCLUDE)
        result: OperationsBrief = schema().load(json, partial=True, unknown=EXCLUDE)
        self.logger.debug('operations @ {} [pg {} of {}] <-'.format(userId, pageNumber, result.paginator.totalPages))

        return result

    def operations_all(self, userId: int) -> List[OperationBrief]:
        return self.all_pages(userId, lambda uid, pageno : self.operations(uid, pageno), lambda content : content.operations)

    def operation_detail(self, userId:int, operationId:int, operationType:str) -> OperationDetail:
        self.logger.debug('operations_detail @ {} [op {} {}] ->'.format(userId, operationId, operationType))
        json = self.execute('POST', 'api/finances/operation/load_data?lang={}'.format(self.lang), json={
            'userId': userId,
            'id':operationId,
            'type': operationType
        })
        schema = marshmallow_dataclass.class_schema(OperationDetail)
        result:OperationDetail = schema().load(json, partial=True, unknown=EXCLUDE)
        self.logger.debug('operations_detail @ {} [op {} {}] <-'.format(userId, operationId, operationType))

        return result

    def add_operation(self, userId:int, op:SetOperation) -> AddEntityResponse:
        exclude = ['operation.date', 'operation.uahDate']
        self.logger.debug('add_operation @ {} ->'.format(userId))
        payload_schema = marshmallow_dataclass.class_schema(AddOperation, base_schema=IgnoreNoneSchema)
        payload:AddOperation = AddOperation(userId, op)
        #print('payload raw ', payload)
        #print('payload json ', payload_schema(exclude=exclude).dumps(payload, ensure_ascii=False))
        json = self.execute('POST', 'api/finances/operation/create?lang={}'.format(self.lang), json=payload_schema(exclude=exclude).dump(payload))
        self.logger.debug('operations_detail @ {} <-'.format(userId))
        schema = marshmallow_dataclass.class_schema(AddEntityResponse)
        return schema().load(json, partial=True, unknown=EXCLUDE)

    def user_accounts(self, userId: int, pageNumber: int = 1) -> UserAccounts:
        self.logger.debug('user_accounts @ {} [pg {}] ->'.format(userId, pageNumber))
        json = self.execute('POST', 'api/finances/account/load?lang={}'.format(self.lang), json={
            'userId': userId,
            'pageNumber': pageNumber,
            'filters': {}
        })
        schema = marshmallow_dataclass.class_schema(UserAccounts)
        result: UserAccounts = schema().load(json, partial=True, unknown=EXCLUDE)
        self.logger.debug('user_accounts @ {} [pg {} of {}] <-'.format(userId, pageNumber, result.paginator.totalPages))
        return result

    def user_accounts_all(self, userId: int) -> List[UserAccount]:
        return self.all_pages(userId, lambda uid, pageno: self.user_accounts(uid, pageno),
                              lambda content: content.accounts)

    def documents(self, userId:int, pageNumber:int = 1) -> UserDocuments:
        json = self.execute('POST', 'api/finances/document/load?lang={}'.format(self.lang), json={
            'userId': userId,
            'pageNumber': pageNumber,
            'filters': {}
        })
        schema = marshmallow_dataclass.class_schema(UserDocuments)
        return schema().load(json)
    def documents_all(self, userId: int) -> List[UserDocuments]:
        return self.all_pages(userId, lambda uid, pageno : self.documents(uid, pageno), lambda content : content.documents)
    def document(self, userId:int, docId:int, docType:str) -> Document:
        json = self.execute('POST', 'api/finances/document/load_data?lang={}'.format(self.lang), json={
            'userId': userId,
            'document': {
                'id' : docId,
                'type': docType
            }
        })
        schema = marshmallow_dataclass.class_schema(Document)
        return schema().load(json)
    def add_document(self, userId:int, doc:Document) -> AddEntityResponse:
        exclude=['document.date', 'document.expireDate']
        self.logger.debug('add_document @ {} ->'.format(userId))
        payload_schema = marshmallow_dataclass.class_schema(AddDocument, base_schema=IgnoreNoneSchema)
        payload:AddDocument = AddDocument(userId, doc)
        #print('payload raw ', payload)
        #print('payload json ', payload_schema(exclude=exclude).dumps(payload, ensure_ascii=False))
        json = self.execute('POST', f'api/finances/document/create?lang={self.lang}', json=payload_schema(exclude=exclude).dump(payload))
        #json = {'id': 1}
        self.logger.debug('add_document @ {} <-'.format(userId))
        schema = marshmallow_dataclass.class_schema(AddEntityResponse)
        return schema().load(json, partial=True, unknown=EXCLUDE)