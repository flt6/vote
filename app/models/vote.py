from app.utils.json_handler import save_json, load_json
from typing import List, Dict

class VoteModel:
    default_data = {
        'title': '',
        'options': [],
        'votes': {},
        'show_count': False
    }
    
    
    def __init__(self):
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        return load_json('data/vote.json') or self.default_data
    
    
    def set_config(self, title: str, options: List[str], show_count: bool):
        self.data['title'] = title
        self.data['options'] = options
        self.data['votes'] = {}
        self.data['show_count'] = show_count
        self._save()
    
    def add_vote(self, option: str) -> bool:
        self.data=self._load_data()
        if option in self.data['options']:
            if option not in self.data['votes']:
                self.data['votes'][option] = 0
            self.data['votes'][option] += 1
            self._save()
            return True
        return False
    
    def get_stats(self) -> Dict:
        self.data=self._load_data()
        total = sum(self.data['votes'].values())
        stats = []
        for option in self.data['options']:
            count = self.data['votes'].get(option, 0)
            stats.append({
                'option': option,
                'count': count,
                'percentage': round(count * 100 / total if total else 0, 1)
            })
        return stats
    
    def _save(self):
        save_json('data/vote.json', self.data)