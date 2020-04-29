from dataclasses import dataclass, field
from typing import Dict, List
from marshmallow import Schema, fields
from marshmallow.utils import EXCLUDE, INCLUDE
from decimal import *
from datetime import datetime
import ujson
#-----------------------------------------------------
@dataclass
class User:
    id:int= field(default=None)
    idKey:str= field(default=None)
    titleName:str= field(default=None)
    isCompany: bool= field(default=None)
    class Meta:
        unknown=EXCLUDE

@dataclass
class Account:
    accountId:int= field(default=None)
    accountName:str= field(default=None)
    users:List[User] = field(default=None)
    class Meta:
        unknown=EXCLUDE



#-----------------------------------------------------
@dataclass
class TimestampContent:
    timestamp:int = field(default=None)
    date:datetime = field(default=None)

    def __post_init__(self):
        if None == self.date and None != self.timestamp:
            self.date = datetime.fromtimestamp(self.timestamp)
        if None == self.timestamp and None != self.date:
            self.timestamp = self.date.timestamp()

    class Meta:
        unknown=EXCLUDE

@dataclass
class ExpireTimestamp:
    expireTimestamp:int = field(default=None)
    expireDate:datetime = field(default=None)

    def __post_init__(self):
        if None == self.expireDate and None != self.expireTimestamp:
            self.expireDate = datetime.fromtimestamp(self.expireTimestamp)
        if None == self.expireTimestamp and None != self.expireDate:
            self.expireTimestamp = self.expireDate.timestamp()

    class Meta:
        unknown=EXCLUDE


@dataclass
class UahTimestampContent:
    uahTimestamp:int = field(default=None)
    uahDate:datetime = field(default=None)

    def __post_init__(self):
        if None == self.uahDate and None != self.uahTimestamp:
            self.uahDate = datetime.fromtimestamp(self.uahTimestamp)
        if None == self.uahTimestamp and None != self.uahDate:
            self.uahTimestamp = self.uahDate.timestamp()

    class Meta:
        unknown=EXCLUDE

@dataclass
class OperationContent(TimestampContent):
    id:int = field(default=None)
    sumCurrency:Decimal = field(default=None)
    accountTitle:str = field(default=None)
    accountCurrency: str = field(default=None)
    comment:str = field(default=None)

    class Meta:
        unknown=EXCLUDE
        #exclude = ['date']

@dataclass
class OperationBrief:
    id:int = field(default=None)
    type:str = field(default=None)
    comment:str = field(default=None)
    contents: List[OperationContent] = field(default=None)

    def __post_init__(self): pass

    class Meta:
        unknown=EXCLUDE


@dataclass
class Paginator:
    currentPage:int = field(default=None)
    recordsOnPage:int = field(default=None)
    totalPages:int = field(default=None)
    class Meta:
        unknown=EXCLUDE


@dataclass
class OperationsBrief:
    paginator: Paginator = field(default=None)
    operations: List[OperationBrief] = field(default=None)
    currencies: List[str] = field(default=None)
    class Meta:
        unknown=EXCLUDE

#-----------------------------------------------------
@dataclass
class OperationAccount:
    id: int = field(default=None)
    title: str = field(default=None)
    currency: str = field(default=None)
    class Meta:
        unknown=EXCLUDE

@dataclass
class ContractorBrief:
    id: int = field(default=None)
    title: str = field(default=None)
    class Meta:
        unknown=EXCLUDE


@dataclass
class Contractor(ContractorBrief):
    juridicalAddress: str = field(default=None)
    class Meta:
        unknown=EXCLUDE

@dataclass
class Document(TimestampContent, ExpireTimestamp):
    id: int= field(default=None)
    type: str= field(default=None) #"contract"
    direction: int = field(default=None) # 0 - продажа, 1 покупка??
    number: str= field(default=None)
    contractor:ContractorBrief= field(default=None)
    currency: str = field(default=None)
    paid: Decimal = field(default=None)
    total: Decimal = field(default=None)
    title: str= field(default=None)
    comment: str= field(default=None)
    description: str = field(default=None)
    place: str = field(default=None)

    """Resolve multiple inheritance"""
    def __post_init__(self):
        TimestampContent.__post_init__(self)
        ExpireTimestamp.__post_init__(self)

    class Meta:
        unknown=EXCLUDE

@dataclass
class Parent(TimestampContent):
    id:int = field(default=None)
    type: str = field(default=None)
    number: str = field(default=None)
    num: str = field(default=None)
    title: str = field(default=None)

    direction:int = field(default=None)
    contractor: ContractorBrief = field(default=None)

    def __post_init__(self):
        if None != self.num and None == self.number:
            self.number = self.num
    class Meta:
        unknown = EXCLUDE
        render_module = ujson

@dataclass
class ExchangeDifference:
    id: int = field(default=None)
    operationId: int = field(default=None)
    total: Decimal = field(default=None)

    class Meta:
        unknown = EXCLUDE
        render_module = ujson

@dataclass
class OperationDetail(OperationBrief, TimestampContent, UahTimestampContent):
    contractor:ContractorBrief = field(default=None)
    parent:Parent = field(default=None)
    payedSum: Decimal = field(default=None)
    financeType: str = field(default=None)
    account: OperationAccount = field(default=None)
    total: Decimal = field(default=None)
    outgoTotal: Decimal = field(default=None)
    outgoAccount: OperationAccount = field(default=None)
    incomeCurrency: Decimal = field(default=None)
    incomeAccount: OperationAccount = field(default=None)

    exchangeDifference: ExchangeDifference = field(default=None)

    uahTotal: Decimal = field(default=None)
    uahAccount: OperationAccount = field(default=None)
    currencyAccount: OperationAccount = field(default=None)
    currencyTotal: Decimal = field(default=None)

    """Resolve multiple inheritance"""
    def __post_init__(self):
        TimestampContent.__post_init__(self)
        UahTimestampContent.__post_init__(self)

    class Meta:
        unknown=EXCLUDE
#-----------------------------------------------------

@dataclass
class UserAccount:
    id: int
    balance: Decimal
    title: str = None
    currency: str = None
    num: str = None
    bank: str = None
    mfo: str = None
    comment: str = None
    tfBankPlace: str = None
    tfBankSwift: str = None
    tfBankCorr: str = None
    tfBankCorrPlace: str = None
    tfBankCorrSwift: str = None
    tfBankCorrAccount: str = None

    class Meta:
        unknown=EXCLUDE

class UserAccounts:
    paginator: Paginator
    accounts: List[UserAccount] = field(default_factory=list)
    accountsCurrencies: List[str] = field(default_factory=list)
    class Meta:
        unknown=EXCLUDE

class UserDocuments:
    paginator: Paginator
    documents: List[Document] = field(default_factory=list)
    class Meta:
        unknown=EXCLUDE


# -----------------------------------------------------
@dataclass
class SetOperation(TimestampContent, UahTimestampContent):
    type: str = field(default=None)
    comment: str = field(default=None)
    outgoTotal: Decimal = field(default=None)
    outgoAccount: OperationAccount = field(default=None)
    incomeAccount: OperationAccount = field(default=None)

    payedSum: Decimal = field(default=None)
    total: Decimal = field(default=None)
    contractor : ContractorBrief = field(default=None)
    account: OperationAccount = field(default=None)
    financeType: str = field(default=None)
    parent: Parent = field(default=None)

    incomeCurrency:Decimal = field(default=None)

    uahTotal: Decimal = field(default=None)
    uahAccount: OperationAccount = field(default=None)
    currencyAccount: OperationAccount = field(default=None)
    currencyTotal: Decimal = field(default=None)


    """Resolve multiple inheritance"""
    def __post_init__(self):
        TimestampContent.__post_init__(self)
        UahTimestampContent.__post_init__(self)

    class Meta:
        unknown = EXCLUDE
        render_module = ujson

@dataclass
class AddOperation:
    userId:int = field(default=None)
    operation: SetOperation = field(default=None)
    class Meta:
        unknown = EXCLUDE
        render_module = ujson

@dataclass
class AddOperationResponse:
    id: int
    class Meta:
        unknown = EXCLUDE
