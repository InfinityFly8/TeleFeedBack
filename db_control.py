import time
from parameters import settings
from models import Id, Banned, Session

session = Session()

class IdManager:    
    def get_chat_id(self, message_id: int):
        session.query(Id).filter(Id.date < (int(time.time()) - settings.DELETE_DELAY)).delete()
        result = session.query(Id).filter_by(message_id=message_id).first()
        try:
            return result.chat_id
        except AttributeError:
            return None
    
    def add_id_pair(self, message_id: int, chat_id: int):
        session.add(Id(message_id, chat_id, int(time.time())))
        session.commit()
    

class Banlist:
    def add(self, id: int, username: str):
        session.add(Banned(id, username))
        session.commit()
    
    def get(self, id: int):
        result = session.query(Banned).filter_by(id=id).first()
        if result:
            return result.id, result.username

    def remove(self, id: int):
        session.query(Banned).filter_by(id=id).delete()
        session.commit()

    def __contains__(self, id: int):
        result = session.query(Banned).filter_by(id=id).first()
        return bool(result)
