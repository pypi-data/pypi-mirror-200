from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin


# @dataclass_json 也可以采用装饰器的方式使用
@dataclass
class DataClassBase(DataClassJsonMixin):
    pass
