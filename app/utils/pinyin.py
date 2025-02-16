from pypinyin import pinyin, Style

def get_pinyin(text: str) -> str:
    return ''.join([p[0] for p in pinyin(text, style=Style.NORMAL)])

def get_pinyin_first(text: str) -> str:
    return ''.join([p[0][0] for p in pinyin(text, style=Style.FIRST_LETTER)])

def pinyinMatch(text: str, search: str) -> bool:
    text_pinyin = get_pinyin(text).lower()
    text_first = get_pinyin_first(text).lower()
    search = search.lower()
    
    return (search in text_pinyin) or (search in text_first)