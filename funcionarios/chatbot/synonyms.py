import re

SYNONYMS = {
    # Departamentos
    "recursos humanos": "rh",
    "recursos humano": "rh",
    "tecnologia da informacao": "ti",
    "tecnologia": "ti",
    "atendimento ao cliente": "atendimento",
    
    # Termos comuns
    "colaborador": "funcionario",
    "colaboradores": "funcionarios",
    "empregado": "funcionario",
    "empregados": "funcionarios",
    
    "remuneracao": "salario",
    "remuneracoes": "salarios",
    "pagamento": "salario",
    "pagamentos": "salarios",
    
    "admitido": "contratado",
    "admitidos": "contratados",
    "admissao": "contratacao",
    
    "departamento": "setor",
    "departamentos": "setores",
    
    "mostrar": "listar",
    "exibir": "listar",
    "ver": "listar",
}

def replace_synonyms(text: str) -> str:
    """
    Substitui sinônimos comuns por seus termos canônicos.
    Substitui primeiro as expressões mais longas para evitar conflitos.
    """
    if not text:
        return ""
    
    # Ordena pelo tamanho da chave de forma decrescente
    sorted_synonyms = sorted(SYNONYMS.items(), key=lambda item: len(item[0]), reverse=True)
    
    for syn, canonical in sorted_synonyms:
        # Usa limite de palavra (\b) para evitar substituir pedaços de palavras
        pattern = r'\b' + re.escape(syn) + r'\b'
        text = re.sub(pattern, canonical, text)
    
    return text
