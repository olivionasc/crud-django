import re
import unicodedata

def normalize_text(text: str) -> str:
    """
    Normaliza o texto do usuário:
    - Converte para minúsculas
    - Remove acentos
    - Remove pontuação
    - Remove espaços extras
    """
    if not text:
        return ""
    # Converte para minúsculas
    text = text.lower()
    # Remove acentos
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    # Remove pontuação (substitui por espaço para não juntar palavras coladas com pontuação)
    text = re.sub(r'[^\w\s]', ' ', text)
    # Remove espaços extras
    text = re.sub(r'\s+', ' ', text).strip()
    return text
