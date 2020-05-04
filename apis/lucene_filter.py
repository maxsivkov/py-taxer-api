from typing import Dict
from luqum.parser import parser
from luqum.pretty import prettify
from luqum import tree as t
import isodate

class Lucene2Filter:
    def __init__(self, s):
        self.s = s
        self.tree = parser.parse(s) if s is not None else None

    def dt2timestamp(self, s, timePortion):
        if not 'T' in s:
            s += f'T{timePortion}'
        return int(isodate.parse_datetime(s).timestamp())

    def dt2timestamp_low(self, s):return self.dt2timestamp(s, '00:00')
    def dt2timestamp_high(self, s): return self.dt2timestamp(s, '23:59')
    def special(self, tree, name:str, low_value:str, high_value:str) -> Dict[str, object]: raise NotImplementedError()
    def l2filter(self, tree) -> Dict[str, object]:
        # print('********     search query', prettify(tree))
        result = {}

        if isinstance(tree, t.AndOperation):
            for op in tree.operands:
                result.update(self.l2filter(op))
        if isinstance(tree, t.SearchField):
            name = str(tree.name)
            if isinstance(tree.expr, t.Range):
                low_value = str(tree.expr.low) if tree.expr.include_low else None
                high_value = str(tree.expr.high) if tree.expr.include_high else None
                result = self.special(tree, name, low_value, high_value)
            if isinstance(tree.expr, t.Word):
                result = {name: str(tree.expr.value)}
            if isinstance(tree.expr, t.Phrase):
                result = {name: str(tree.expr.value).strip('"')}
        return result

    def filter(self):
        return self.l2filter(self.tree) if self.tree is not None else {}

