from datetime import datetime
from ..storages.storage import Storage
from ..notifier import Notifier

class GAsset():

    storage = Storage()
    notifier = Notifier()

    def __init__(self, name, messageType, title=None, description=None, var=None, show=True) -> None:
        self.name = name
        self.messageType = messageType
        self.title = title
        self.description = description
        self.var = var
        self.created = datetime.now()
        self.modified = self.created
        self.show = show

    def to_json(self):

        result ={
            "name": self.name,
            "messageType": self.messageType,
            "title": self.title,
            "description": self.description,
            "var": self.var,
            "created": str(self.created),
            "modified": str(datetime.now()),
            "show": self.show
        }
        return result
    
    def get_path(self):
        return None
    
    def send(self):
        self.storage.save(path=self.get_path(), metadata=self.to_json())
        self.notifier.something_has_changed(self.to_json())
