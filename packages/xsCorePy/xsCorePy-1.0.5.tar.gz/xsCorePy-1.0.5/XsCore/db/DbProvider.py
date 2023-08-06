from enum import Enum

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session


class DataBaseType(Enum):
    sqlite = 1
    mysql = 2

Base = declarative_base()
class DbProvider:
    def __init__(self,dbtype: DataBaseType):
        self.engine = create_engine('sqlite:///db.db?check_same_thread=False', echo=True)

        # 创建Session类实例
        db_session = scoped_session(sessionmaker(autocommit=False,
                                                 autoflush=False,
                                                 bind=self.engine))


        # Session = sessionmaker(bind=self.engine)
        self.session = db_session

        # Base.query = db_session.query_property()

    def create_all_table(self):
        Base.metadata.create_all(self.engine)  # 创建表结构

db_provider = DbProvider(DataBaseType.sqlite)
