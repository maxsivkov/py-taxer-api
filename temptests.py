from typing import ClassVar, Type, Optional, Dict, List
from dataclasses import field
from decimal import *
from datetime import datetime
import isodate
import ujson
import json
from marshmallow import Schema
from marshmallow.utils import EXCLUDE, INCLUDE
from marshmallow_dataclass import dataclass, class_schema

from luqum.parser import parser
from luqum.pretty import prettify
from luqum import tree as t

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

def q2filter(tree) -> Dict[str,object]:
    print('********     search query', prettify(tree))
    result = {}
    def dt2timestamp(s, timePortion):
        if not 'T' in s:
            s += f'T{timePortion}'
        return int(isodate.parse_datetime(s).timestamp())

    if isinstance(tree, t.AndOperation):
        for op in tree.operands:
            result.update(q2filter(op))
    if isinstance(tree, t.SearchField):
        name = str(tree.name)
        if isinstance(tree.expr, t.Range):
            low_value = str(tree.expr.low) if tree.expr.include_low else None
            high_value = str(tree.expr.high) if tree.expr.include_high else None
            if name == 'filterDate':
                result = {name: {'dateFrom':dt2timestamp(low_value, '00:00'), 'dateTo':dt2timestamp(high_value, '23:59')}}
            if name == 'filterTotal':
                expr = None
                if tree.expr.include_low and tree.expr.include_high and low_value == high_value:
                    expr = f'equal-{low_value}'
                elif low_value != '*':
                    expr = f'more-{low_value}'
                elif high_value != '*':
                    expr = f'less-{high_value}'
                result = {name: expr}
        if isinstance(tree.expr, t.Word):
            result = {name: str(tree.expr.value)}
        if isinstance(tree.expr, t.Phrase):
            result = {name: str(tree.expr.value).strip('"')}
    return result

def traverse_q():
    q = 'filterType:"FlowIncome" AND filterDate:[2020-04-01 TO 2020-05-01] AND filterTotal:[200 TO *] AND filterCurrency:USD AND filterAccount:2 AND filterComment:"123"'
    tree = parser.parse(q)
    res = q2filter(tree)
    json1 = ujson.dumps(res)
    print(json1)
