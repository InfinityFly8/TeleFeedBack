from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, MetaData, ForeignKey
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker
from parameters import settings

engine = create_engine(settings.DB_ACCESS, echo=True, pool_recycle=7200)
Session = sessionmaker()
Session.configure(bind=engine)

metadata = MetaData()

id_table = Table('chats', metadata,
    Column('message_id', Integer, ForeignKey('banned_users.id'), primary_key=True),
    Column('chat_id', Integer),
    Column('date', Integer)
)

ban_table = Table('banned_users', metadata,
    Column('id', Integer, ForeignKey('chats.chat_id'), primary_key=True)
)


class Id:
    def __init__(self, message_id: int, chat_id: int,date: int):
        self.message_id = message_id
        self.chat_id = chat_id
        self.date = date
    def __repr__(self):
        return "Id(message_id={}, chat_id={}, date={})".format(self.message_id,
                                                               self.chat_id,
                                                               self.date)


class Banned:
    def __init__(self, id):
        self.id = id
    def __repr__(self):
        return "BannedUser(id=%s)".format(self.id)


metadata.create_all(engine)
mapper(Id, id_table)
mapper(Banned, ban_table)
