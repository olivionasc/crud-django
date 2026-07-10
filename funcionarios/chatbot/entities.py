import re
import datetime
from funcionarios.models import Funcionario
from .normalization import normalize_text
from .fuzzy import levenshtein_distance
from .synonyms import replace_synonyms

def extract_entities(text: str) -> dict:
    """
    Extrai entidades do texto da pergunta:
    - Nome do funcionário
    - Setor/Departamento
    - Cargo
    - Valor de Salário e operador (maior, menor, igual)
    - Ano/Data
    - Status ativo/inativo
    """
    # 1. Buscar dados dinâmicos do banco
    dept_choices = Funcionario.DEPARTAMENTO_CHOICES
    
    # Obter cargos e nomes distintos cadastrados no BD
    try:
        cargos = list(Funcionario.objects.values_list('cargo', flat=True).distinct())
        nomes = list(Funcionario.objects.values_list('nome', flat=True))
    except Exception:
        cargos = []
        nomes = []

    cargos_normalized = {normalize_text(c): c for c in cargos if c}
    nomes_normalized = {normalize_text(n): n for n in nomes if n}

    entities = {
        "name": None,
        "department": None,
        "cargo": None,
        "salary_value": None,
        "salary_operator": None,  # 'greater', 'less', 'equal'
        "year": None,
        "active": None,
    }

    # Normalizar e aplicar sinônimos ao texto de entrada do usuário
    normalized_text = replace_synonyms(normalize_text(text))

    # 2. Extrair operador e valor de salário
    # Ex: "mais de 8000", "maior que 8.000", "acima de R$ 8.000,00"
    salary_greater = re.search(r'(?:mais\s+de|maior\s+que|acima\s+de|>)\s*(?:rs\s*)?(\d+(?:[\.,]\d+)?)', normalized_text)
    if salary_greater:
        val_str = salary_greater.group(1).replace('.', '').replace(',', '.')
        try:
            entities["salary_value"] = float(val_str)
            entities["salary_operator"] = "greater"
        except ValueError:
            pass

    if not entities["salary_value"]:
        # Ex: "menos de 5000", "menor que 5.000", "abaixo de R$ 5.000,00"
        salary_less = re.search(r'(?:menos\s+de|menor\s+que|abaixo\s+de|<)\s*(?:rs\s*)?(\d+(?:[\.,]\d+)?)', normalized_text)
        if salary_less:
            val_str = salary_less.group(1).replace('.', '').replace(',', '.')
            try:
                entities["salary_value"] = float(val_str)
                entities["salary_operator"] = "less"
            except ValueError:
                pass

    if not entities["salary_value"]:
        # Ex: "recebe 8000", "ganha 5000"
        salary_equal = re.search(r'(?:recebe|ganha|salario|pagamento)\s+(?:de\s+)?(?:rs\s*)?(\d+(?:[\.,]\d+)?)', normalized_text)
        if salary_equal:
            val_str = salary_equal.group(1).replace('.', '').replace(',', '.')
            try:
                entities["salary_value"] = float(val_str)
                entities["salary_operator"] = "equal"
            except ValueError:
                pass

    # 3. Extrair ano (ex: "2023", "2026")
    year_match = re.search(r'\b(20\d{2}|19\d{2})\b', normalized_text)
    if year_match:
        entities["year"] = int(year_match.group(1))
    elif "este ano" in normalized_text or "ano atual" in normalized_text:
        entities["year"] = datetime.datetime.now().year

    # 4. Extrair status ativo/inativo
    if "inativo" in normalized_text:
        entities["active"] = False
    elif "ativo" in normalized_text:
        entities["active"] = True

    # 5. Extrair departamento/setor
    for code, label in dept_choices:
        norm_label = normalize_text(label)
        norm_code = normalize_text(code)
        if norm_label in normalized_text or norm_code in normalized_text:
            entities["department"] = code
            break

    if not entities["department"]:
        # Fuzzy match de palavras no texto para departamentos
        for word in normalized_text.split():
            for code, label in dept_choices:
                norm_label = normalize_text(label)
                norm_code = normalize_text(code)
                if levenshtein_distance(word, norm_code) <= 1 or levenshtein_distance(word, norm_label) <= 1:
                    entities["department"] = code
                    break
            if entities["department"]:
                break

    # 6. Extrair cargo
    sorted_cargos = sorted(cargos_normalized.items(), key=lambda x: len(x[0]), reverse=True)
    for norm_cargo, orig_cargo in sorted_cargos:
        if norm_cargo in normalized_text:
            entities["cargo"] = orig_cargo
            break

    if not entities["cargo"]:
        # Fuzzy matching por palavra para cargos
        for word in normalized_text.split():
            if len(word) <= 3:
                continue
            for norm_cargo, orig_cargo in sorted_cargos:
                # Se for similar ao cargo inteiro ou a partes dele
                parts = norm_cargo.split()
                if any(levenshtein_distance(word, p) <= 1 for p in parts if len(p) > 3):
                    entities["cargo"] = orig_cargo
                    break
            if entities["cargo"]:
                break

    # 7. Extrair nome do funcionário
    sorted_names = sorted(nomes_normalized.items(), key=lambda x: len(x[0]), reverse=True)
    for norm_name, orig_name in sorted_names:
        if len(norm_name) > 3 and norm_name in normalized_text:
            entities["name"] = orig_name
            break

    if not entities["name"]:
        # Fuzzy match para partes de nomes ou nomes completos com pequenos erros
        words_in_text = [w for w in normalized_text.split() if len(w) > 2]
        for norm_name, orig_name in sorted_names:
            words_in_name = norm_name.split()
            matched_words = 0
            for nw in words_in_name:
                if len(nw) > 2:
                    if any(levenshtein_distance(nw, tw) <= 1 for tw in words_in_text):
                        matched_words += 1
            # Se bateu a maior parte do nome completo
            if len(words_in_name) > 0 and matched_words == len(words_in_name):
                entities["name"] = orig_name
                break
            # Caso seja apenas o primeiro nome fornecido
            elif len(words_in_name) > 0 and matched_words >= 1 and words_in_name[0] in words_in_text:
                entities["name"] = orig_name
                break

    return entities
