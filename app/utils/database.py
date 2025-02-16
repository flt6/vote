from .json_handler import load_json,save_json
from pathlib import Path
from typing import Callable
from threading import Thread
import time
import atexit

_dataFile=Path("data.json")

class _data:
    def __init__(self,d:dict,savefunc:Callable[[],None]):
        self.d = d
        self._save=savefunc

    def __setitem__(self, key, value):
        self.d.__setitem__(key, value)
        self._save()
    
    def __getitem__(self,key):
        return self.d[key]

    def items(self):
        return self.d.items()
    
    def reset(self,m):
        self.d.clear()
        self.d.update(m)
        self._save()
    

class Database:
    def __init__(self):
        if _dataFile.exists():
            self._data = load_json(_dataFile)
        else:
            self._data = {}
            self._save()
            
        self._run = True
        Thread(target=self._call_save,daemon=True).start()
    
    def _call_save(self):
        while self._run:
            time.sleep(10)
            self._save()
    
    def __del__(self):
        self._run = False
    
    def _save(self):
        save_json(_dataFile,self._data)
    
    def get(self,name:str,default:dict={}) -> _data:
        if name not in self._data.keys():
            self._data[name]=default
            self._save()
        return _data(self._data[name],self._save)

@atexit.register
def _save():db._save()

db = Database()
