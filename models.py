from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from parameters import settings

engine = create_engine(settings.DB_ACCESS, echo=True, pool_recycle=7200)
Base = declarative_base()

class Id(Base):
    __tablename__ = 'chats'
    message_id = Column('message_id', Integer, ForeignKey('banned_users.id'), primary_key=True)
    chat_id = Column('chat_id', Integer)
    date = Column('date', Integer)

    def __init__(self, message_id: int, chat_id: int,date: int):
        self.message_id = message_id
        self.chat_id = chat_id
        self.date = date
    
    def __repr__(self):
        return "Id(message_id={}, chat_id={}, date={})".format(self.message_id,
                                                               self.chat_id,
                                                               self.date)


class Banned(Base):
    __tablename__ = 'banned_users'
    id = Column('id', Integer, ForeignKey('chats.chat_id'), primary_key=True)
    username = Column('username', String)

    def __init__(self, id: int, username: str):
        self.id = id
        self.username = username
    
    def __repr__(self):
        return "Banned(id={}, username={})".format(self.id, self.username)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

