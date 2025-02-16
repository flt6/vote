import json
from pathlib import Path
from typing import Dict, Any

def load_json(filepath: Path) -> Dict:
    if not filepath.exists():
        return None
    return json.loads(filepath.read_text())

def save_json(filepath: Path, data: Any):
    filepath.write_text(json.dumps(data, ensure_ascii=False, indent=2))