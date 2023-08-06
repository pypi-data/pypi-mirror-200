from hawa.base.db import MongoUtil
from hawa.config import project


def prepare_test():
    project.COMPLETED = True
    MongoUtil.connect()


def validate_data_for_web(d):
    """校验数据是否可以被 web 响应"""
    match str(type(d)):
        case "<class 'str'>" | "<class 'int'>" | "<class 'float'>":
            pass
        case "<class 'list'>":
            for item in d:
                validate_data_for_web(item)
        case "<class 'dict'>" | "<class 'collections.defaultdict'>":
            for v in d.values():
                validate_data_for_web(v)
        case _:
            raise TypeError(f'不支持的类型 {type(d)}')
