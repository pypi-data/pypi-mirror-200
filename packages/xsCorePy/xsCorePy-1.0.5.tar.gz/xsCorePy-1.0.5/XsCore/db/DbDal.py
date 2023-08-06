# from typing import Generic, TypeVar

from sqlalchemy import create_engine, select, exists, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from XsCore.db import Base, db_provider

# T = TypeVar("T")
from tests.db.UserEntity import UserEntity


class DbDal:

    def __init__(self, MT):
        self.engine = db_provider.engine
        self.__MT = MT

    def add(self, model: Base):
        with Session(self.engine) as session:
            session.add(model)
            session.commit()

    def addList(self, models: list):
        with Session(self.engine) as session:
            session.add_all(models)
            session.commit()

    def getOne(self, data_id):
        with Session(self.engine) as session:
            return session.query(self.__MT).filter_by(id=data_id).first()

    def getOneWhere(self, **where):
        with Session(self.engine) as session:
            return session.query(self.__MT).filter_by(**where).first()

    def getAll(self, *orderBy):
        with Session(self.engine) as session:
            return session.query(self.__MT).order_by(*orderBy)

    def getList(self, where, orderBy=None):
        with Session(self.engine) as session:
            return session.query(self.__MT).filter(where).order_by(orderBy)

    def getTop(self, num):
        with Session(self.engine) as session:
            return session.query(self.__MT).order_by(self.__MT.id.desc()).limit(num)

    def getPageWhere(self, page_index, page_size, where, orderBy=None):
        with Session(self.engine) as session:
            return session.query(self.__MT).filter(where).order_by(orderBy).limit(page_size).offset(
                (page_index - 1) * page_size)

    def getPageAll(self, page_index, page_size, orderBy=None):
        with Session(self.engine) as session:
            return session.query(self.__MT).order_by(orderBy).limit(page_size).offset(
                (page_index - 1) * page_size)

    def existsId(self, data_id):
        with Session(self.engine) as session:
            return session.query(exists().where(self.__MT.id == data_id)).scalar()

    def exists(self, *where):
        with Session(self.engine) as session:
            return session.query(exists().where(*where)).scalar()

    def getMaxId(self):
        with Session(self.engine) as session:
            return session.query(func.max(self.__MT.id)).scalar()

    def getCountAll(self):
        with Session(self.engine) as session:
            return session.query(func.count(self.__MT.id)).scalar()

    def getCountWhere(self, *where):
        with Session(self.engine) as session:
            return session.query(func.count(self.__MT.id)).filter(*where).scalar()

    def delId(self, data_id):
        with Session(self.engine) as session:
            session.query(self.__MT).filter_by(id=data_id).delete()
            session.commit()

    def delWhere(self, **where):
        with Session(self.engine) as session:
            session.query(self.__MT).filter_by(**where).delete()
            session.commit()

    def delAll(self):
        with Session(self.engine) as session:
            session.query(self.__MT).delete()
            session.commit()
