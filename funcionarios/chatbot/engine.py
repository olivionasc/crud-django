from .normalization import normalize_text
from .synonyms import replace_synonyms
from .fuzzy import correct_sentence_words
from .intent import detect_intent
from .entities import extract_entities
from .query import execute_query
from .response import generate_response

# Palavras-chave principais para correção ortográfica (Fuzzy Matching)
KEYWORD_TARGETS = [
    "funcionario", "funcionarios", "colaborador", "colaboradores", "empregado", "empregados",
    "salario", "salarios", "remuneracao", "remuneracoes", "pagamento", "pagamentos",
    "departamento", "departamentos", "setor", "setores",
    "ativo", "ativos", "inativo", "inativos",
    "contratado", "contratada", "contratados", "admitido", "admitida", "admitidos",
    "listar", "mostrar", "exibir", "todos", "todas",
    "media", "medio", "mediana",
    "maior", "maximo", "mais", "alto",
    "menor", "minimo", "menos", "baixo",
    "contar", "quantidade", "quantos", "total", "numero", "gerente", "desenvolvedor",
    "tecnologia", "informacao", "recursos", "humanos"
]

def process_message(user_message: str) -> str:
    """
    Orquestra o pipeline de NLP para processar a mensagem do usuário
    e retornar a resposta final do chatbot.
    """
    # 1. Normalização do texto
    normalized = normalize_text(user_message)
    if not normalized:
        return "Olá! Como posso ajudar você hoje? Pergunte-me algo sobre os funcionários, setores ou salários."

    # 2. Correção Ortográfica por Fuzzy Matching das palavras-chave
    corrected = correct_sentence_words(normalized, KEYWORD_TARGETS)

    # 3. Dicionário de Sinônimos
    synonym_mapped = replace_synonyms(corrected)

    # 4. Extração de Entidades
    entities = extract_entities(synonym_mapped)

    # 5. Identificação da Intenção
    has_dept = entities["department"] is not None
    has_cargo = entities["cargo"] is not None
    has_name = entities["name"] is not None
    
    intent = detect_intent(
        synonym_mapped, 
        has_department=has_dept, 
        has_cargo=has_cargo, 
        has_name=has_name
    )

    # 6. Execução da Consulta Dinâmica no Banco de Dados
    query_result = execute_query(intent, entities)

    # 7. Geração de Resposta Amigável
    response = generate_response(query_result)

    return response
