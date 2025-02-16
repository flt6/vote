from typing import List, Dict
from app.utils.database import db

class VoteModel:
    default_data = {
        'title': '',
        'options': [],
        'votes': {},
        'show_count': False
    }
    
    
    def __init__(self):
        self.data = db.get("vote", self.default_data)
    
    def set_config(self, title: str, options: List[str], show_count: bool):
        self.data['title'] = title
        self.data['options'] = options
        self.data['votes'] = {}
        self.data['show_count'] = show_count
    
    def add_vote(self, option: str) -> bool:
        if option in self.data['options']:
            if option not in self.data['votes']:
                self.data['votes'][option] = 0
            self.data['votes'][option] += 1
            return True
        return False
    
    def get_stats(self) -> Dict:
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
    
    def reset(self):
        self.data.reset(self.default_data)

vote_model = VoteModel()