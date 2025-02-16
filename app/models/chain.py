from datetime import datetime
from typing import List, Dict
from app.utils.database import db


class ChainModel:
    default_data={
        'names': [],
        'chained': {}
    }
    
    def __init__(self):
        self.data = db.get("chain", self.default_data)
    
    def set_names(self, names: List[str]):
        self.data['names'] = names
        self.data['chained'] = {}
    
    def add_chain(self, name: str) -> bool:
        if name in self.data['names']:
            self.data['chained'][name] = datetime.now().strftime("%m.%d %H:%M")
            return True
        return False
    
    def remove_chain(self, name: str) -> bool:
        if name in self.data['chained']:
            del self.data['chained'][name]
            self.data._save()
            return True
        return False

    def reset(self):
        self.data.reset(self.default_data)
    
    def get_stats(self) -> Dict:
        chained = [{"name":n,"time":t} for n,t in self.data['chained'].items()]
        unchained = [n for n in self.data['names'] if n not in self.data['chained'].keys()]
        return {
            'chained': chained,
            'unchained': unchained,
            'chained_count': len(chained),
            'unchained_count': len(unchained)
        }

chain_model = ChainModel()