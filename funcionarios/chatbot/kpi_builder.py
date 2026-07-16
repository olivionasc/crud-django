from funcionarios.models import Funcionario
from .response import format_currency

def build_kpi(intent: str, query_result: dict) -> dict:
    """
    Constrói o dicionário de dados de um componente KPI.
    """
    data = query_result.get("data")
    entities = query_result.get("entities", {})

    title = "Indicador"
    value = data

    if intent == "media_salarial":
        title = "Salário Médio"
        if entities.get("department"):
            title += f" ({entities['department'].upper()})"
        value = format_currency(data)
    elif intent == "maior_salario":
        title = "Maior Salário"
        if data:
            value = f"{format_currency(data.salario)} - {data.nome}"
        else:
            value = "N/A"
    elif intent == "menor_salario":
        title = "Menor Salário"
        if data:
            value = f"{format_currency(data.salario)} - {data.nome}"
        else:
            value = "N/A"
    elif intent == "contar_funcionarios":
        title = "Quantidade de Funcionários"
        if entities.get("department"):
            title += f" ({entities['department'].upper()})"
        if entities.get("active") is True:
            title += " (Ativos)"
        elif entities.get("active") is False:
            title += " (Inativos)"
        value = data

    return {
        "type": "kpi",
        "title": title,
        "value": value
    }
