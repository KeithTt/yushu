from contextlib import contextmanager
from datetime import datetime

__author__ = 'KeithTt'

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from sqlalchemy import Column, SmallInteger, Integer

# 定义一个子类，继承父类
class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


# 实例化一个对象
db = SQLAlchemy()

# 定义一个基类模型，在基类模型里面继承db.Model，其他模型继承Base
class Base(db.Model):
    # 不创建Base表，让Base模型仅作为基类模型
    __abstract__ = True
    create_time = Column('create_time', Integer)
    # 定义一个status属性控制数据是否被删除，默认为1表示不删除
    status = Column(SmallInteger, default=1)

    def __init__(self):
        # 将执行时间赋值给create_time
        self.create_time = int(datetime.now().timestamp())

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)
