from .normalization import normalize_text
from .synonyms import replace_synonyms
from .fuzzy import correct_sentence_words
from .intent import detect_intent
from .entities import extract_entities
from .query import execute_query
from .response import generate_response
from .response_builder import build_structured_response

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

def process_message(user_message: str) -> dict:
    """
    Orquestra o pipeline de NLP para processar a mensagem do usuário
    e retornar a resposta estruturada final do chatbot.
    """
    return build_structured_response(user_message)

