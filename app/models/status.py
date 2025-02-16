from .chain import chain_model
from ..utils.database import db
from enum import Enum

class Status(Enum):
    CONFIG = 1
    VOTE   = 2
    CHAIN  = 3


class StatusModel:
    def __init__(self):
        self._db = db.get("status",{"status":1})
    
    def set(self,s:Status):
        self._db["status"] = s.value
    
    def get(self):
        return Status(self._db["status"])
    
status_model = StatusModel()