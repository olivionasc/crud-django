def decide_response_type(text: str, intent: str, query_result: dict) -> str:
    """
    Decide qual o tipo de componente visual que melhor se adapta à resposta
    do assistente. Retorna um dos seguintes tipos:
    'dashboard', 'bar-chart', 'pie-chart', 'line-chart', 'card', 'kpi', 'table', 'list', 'text'
    """
    # normalizar o texto para garantir comparações limpas
    text_clean = text.lower().strip()

    # 1. Dashboard
    if any(k in text_clean for k in ["resumo", "dashboard", "visao geral", "analise da empresa", "indicadores"]):
        return "dashboard"

    # 2. Gráficos de Barras
    if any(k in text_clean for k in [
        "funcionarios por setor", 
        "funcionarios por departamento", 
        "colaboradores por setor",
        "funcionarios por cargo", 
        "colaboradores por cargo",
        "salario medio por setor", 
        "media salarial por setor",
        "salario medio por departamento",
        "funcionarios ativos por departamento",
        "funcionarios ativos por setor"
    ]):
        return "bar-chart"

    # 3. Gráficos de Pizza
    if any(k in text_clean for k in [
        "distribuicao por cargo", 
        "distribuicao por setor", 
        "distribuicao por departamento",
        "ativos x inativos", 
        "ativos e inativos", 
        "ativos vs inativos", 
        "ativos/inativos",
        "situacao dos funcionarios"
    ]):
        return "pie-chart"

    # 4. Gráficos de Linha
    if any(k in text_clean for k in [
        "contratacoes ao longo do tempo", 
        "evolucao do numero de funcionarios", 
        "evolucao do numero de colaboradores",
        "crescimento da empresa",
        "contratacoes por mes",
        "contratacoes por ano"
    ]):
        return "line-chart"

    # 5. Card de Funcionário Único
    if intent in ["buscar_funcionario", "dados_completos"] or query_result.get("type") == "single":
        if query_result.get("data") is not None:
            return "card"

    # 6. KPI (Indicadores Simples)
    if intent in ["media_salarial", "maior_salario", "menor_salario", "contar_funcionarios"]:
        return "kpi"

    # 7. Tabela (Listagem Geral)
    if intent == "listar_funcionarios":
        return "table"

    # 8. Lista de Funcionários
    if intent in ["listar_por_setor", "listar_por_cargo"] or query_result.get("type") == "list":
        return "list"

    return "text"
