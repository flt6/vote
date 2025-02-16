from datetime import datetime
from app.utils.json_handler import save_json, load_json
from typing import List, Dict


class ChainModel:
    default_data={
        'names': [],
        'chained': {}
    }
    
    def __init__(self):
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        return load_json('data/chain.json') or self.default_data
    
    def set_names(self, names: List[str]):
        self.data = self._load_data()
        self.data['names'] = names
        self.data['chained'] = {}
        self._save()
    
    def add_chain(self, name: str) -> bool:
        self.data = self._load_data()
        if name in self.data['names']:
            self.data['chained'][name] = datetime.now().strftime("%m.%d %H:%M")
            self._save()
            return True
        return False
    
    def remove_chain(self, name: str) -> bool:
        self.data = self._load_data()
        if name in self.data['chained']:
            del self.data['chained'][name]
            self._save()
            return True
        return False
    
    def get_stats(self) -> Dict:
        self.data = self._load_data()
        chained = [{"name":n,"time":t} for n,t in self.data['chained'].items()]
        unchained = [n for n in self.data['names'] if n not in self.data['chained'].keys()]
        return {
            'chained': chained,
            'unchained': unchained,
            'chained_count': len(chained),
            'unchained_count': len(unchained)
        }
    
    def _save(self):
        save_json('data/chain.json', self.data)
        