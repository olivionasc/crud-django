def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Calcula a distância de Levenshtein entre duas strings.
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def match_word(word: str, targets: list[str]) -> str | None:
    """
    Encontra o melhor correspondente para uma palavra dentro de uma lista de alvos,
    utilizando a distância de Levenshtein com limites proporcionais ao tamanho.
    """
    if not word or not targets:
        return None

    best_match = None
    min_dist = float('inf')

    for target in targets:
        dist = levenshtein_distance(word, target)
        if dist < min_dist:
            # Regras de limite proporcional
            limit = 0
            if len(target) > 6:
                limit = 2
            elif len(target) > 3:
                limit = 1
            
            if dist <= limit:
                min_dist = dist
                best_match = target

    return best_match


def correct_sentence_words(text: str, targets: list[str]) -> str:
    """
    Divide o texto em palavras e tenta corrigir cada uma com base na lista de targets.
    """
    words = text.split()
    corrected_words = []
    for w in words:
        match = match_word(w, targets)
        if match:
            corrected_words.append(match)
        else:
            corrected_words.append(w)
    return " ".join(corrected_words)
