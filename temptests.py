from typing import ClassVar, Type, Optional, Dict, List
from dataclasses import field
from decimal import *
from datetime import datetime
import ujson
from marshmallow import Schema
from marshmallow.utils import EXCLUDE, INCLUDE
from marshmallow_dataclass import dataclass, class_schema

@dataclass
class base:
    id:int = field(default=None)
    type:str = field(default=None)
    comment:str = field(default=None)
    Schema: ClassVar[Type[Schema]] = Schema
    class Meta:
        unknown=EXCLUDE
        render_module = ujson

@dataclass
class class1:
    id:int = field(default=None)
    title: str = field(default=None)
    currency: str = field(default=None)
    class Meta:
        unknown=EXCLUDE
        render_module = ujson

@dataclass
class derived(base):
    @property
    def date(self) -> datetime:
        return datetime.fromtimestamp(self.timestamp)

    @date.setter
    def date(self, x: datetime):
        self.timestamp = x.timestamp()

    #date: datetime.datetime = field(default=None)
    timestamp: int = field(default=None)
    outgoTotal: Decimal = field(default=None)
    outgoAccount: class1 = field(default=None)
    incomeAccount: class1 = field(default=None)
    list: List[class1] = field(default_factory=list)

    Schema: ClassVar[Type[Schema]] = Schema
    #def __post_init__(self):
    #    self.timestamp = int(self.date.timestamp())

    class Meta:
        unknown = EXCLUDE
        #exclude = ['date']
        #include = ['timestamp']
        render_module = ujson


def serialize():
    schema = class_schema(derived, base_schema=base.Schema)

    #jsond:Dict = ujson.loads('')
    #dump_only=["timestamp"]
    op:derived = schema().load({"timestamp": 100, "outgoTotal": 12.12, "outgoAccount" : {"id":10, "title" : "abc", "currency" : "UAH"}, "list":[{"id":1, "title" : "1", "currency" : "UAH1"}, {"id":2, "title" : "2", "currency" : "UAH2"}]})
    print(op)
    s = schema(exclude=['date']).dumps(op)
    print(s)

