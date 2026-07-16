from .normalization import normalize_text
from .synonyms import replace_synonyms
from .fuzzy import correct_sentence_words
from .entities import extract_entities
from .intent import detect_intent
from .query import execute_query
from .response import generate_response
from .decision_engine import decide_response_type
from .kpi_builder import build_kpi
from .chart_builder import build_chart
from .table_builder import build_table
from .dashboard_builder import build_dashboard
from .response import format_date, format_currency, get_display_name

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

def build_structured_response(user_message: str) -> dict:
    """
    Orquestra o processamento da mensagem do usuário e constrói a resposta
    estruturada com os metadados do componente visual correspondente.
    """
    # 1. Normalização do texto
    normalized = normalize_text(user_message)
    if not normalized:
        return {
            "type": "text",
            "text": "Olá! Como posso ajudar você hoje? Pergunte-me algo sobre os funcionários, setores ou salários.",
            "components": [],
            "data": None
        }

    # 2. Correção Ortográfica
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

    # 7. Decidir o tipo do componente visual
    response_type = decide_response_type(user_message, intent, query_result)

    # 8. Geração da resposta amigável em texto
    friendly_text = generate_response(query_result)

    # 9. Construção do componente visual apropriado
    components = []
    
    if response_type == "dashboard":
        dash = build_dashboard()
        components = dash["components"]
    elif response_type == "kpi":
        kpi = build_kpi(intent, query_result)
        components.append(kpi)
    elif response_type in ["bar-chart", "pie-chart", "line-chart"]:
        chart = build_chart(response_type, user_message)
        components.append(chart)
    elif response_type == "table":
        table = build_table(intent, query_result.get("data"))
        components.append(table)
    elif response_type == "card":
        f = query_result.get("data")
        if f:
            components.append({
                "type": "card",
                "title": f.nome,
                "data": {
                    "nome": f.nome,
                    "cargo": f.cargo,
                    "setor": get_display_name('departamento', f.departamento),
                    "salario": format_currency(f.salario),
                    "admissao": format_date(f.data_admissao),
                    "telefone": f.telefone,
                    "email": f.email,
                    "ativo": "Ativo" if f.ativo else "Inativo"
                }
            })
    elif response_type == "list":
        funcs = query_result.get("data") or []
        items = []
        for item in funcs:
            items.append({
                "nome": item.nome,
                "cargo": item.cargo,
                "setor": get_display_name('departamento', item.departamento)
            })
        components.append({
            "type": "list",
            "title": "Colaboradores Encontrados",
            "items": items
        })

    # Preparar dados brutos adicionais se houverem
    raw_data = None
    if query_result.get("type") == "value":
        raw_data = query_result.get("data")

    return {
        "type": response_type,
        "text": friendly_text,
        "components": components,
        "data": raw_data
    }
