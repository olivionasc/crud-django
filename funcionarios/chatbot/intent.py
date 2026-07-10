def detect_intent(text: str, has_department: bool = False, has_cargo: bool = False, has_name: bool = False) -> str:
    """
    Identifica a intenção principal da pergunta do usuário baseando-se no texto normalizado
    e na presença de entidades extraídas.
    """
    # Média Salarial
    if ("media" in text or "medio" in text) and ("salario" in text or "salarial" in text or "remuneracao" in text or "pagamento" in text):
        return "media_salarial"
    
    # Maior Salário
    if ("maior" in text or "maximo" in text or "mais" in text or "alto" in text) and ("salario" in text or "recebe" in text or "ganha" in text or "remuneracao" in text or "pagamento" in text):
        return "maior_salario"
        
    # Menor Salário
    if ("menor" in text or "minimo" in text or "menos" in text or "baixo" in text) and ("salario" in text or "recebe" in text or "ganha" in text or "remuneracao" in text or "pagamento" in text):
        return "menor_salario"
        
    # Contar Funcionários
    if any(q in text for q in ["quantos", "quantidade", "total", "numero"]) and ("funcionario" in text or "colaborador" in text or "empregado" in text or "pessoas" in text or "ativo" in text or "inativo" in text or "cadastrado" in text):
        return "contar_funcionarios"

    # Funcionário contratado mais recentemente
    if ("contratado" in text or "admitido" in text or "admissao" in text or "entrou" in text or "trabalhar" in text) and ("recente" in text or "ultimo" in text or "este ano" in text or "recentemente" in text or "novo" in text):
        return "contratado_recentemente"

    # Funcionário contratado há mais tempo
    if ("contratado" in text or "admitido" in text or "admissao" in text or "entrou" in text or "trabalhar" in text) and ("tempo" in text or "primeiro" in text or "antigo" in text or "antigamente" in text or "comecou" in text):
        return "contratado_antigamente"

    # Dados completos
    if any(d in text for d in ["dados", "detalhes", "completo", "ficha", "tudo", "perfil"]) and has_name:
        return "dados_completos"

    # Buscar funcionário
    if any(b in text for b in ["buscar", "busca", "encontrar", "procura", "pesquisa", "quem e", "quem e o", "quem e a"]) and has_name:
        return "buscar_funcionario"

    # Listar por Setor
    if has_department and ("quem" in text or "listar" in text or "mostrar" in text or "exibir" in text or "trabalha" in text or "setor" in text or "departamento" in text or "todos" in text):
        return "listar_por_setor"

    # Listar por Cargo
    if has_cargo and ("quem" in text or "listar" in text or "mostrar" in text or "exibir" in text or "cargo" in text or "trabalha" in text or "todos" in text):
        return "listar_por_cargo"

    # Listar funcionários (geral)
    if any(l in text for l in ["listar", "lista", "mostrar", "exibir", "todos", "todas"]):
        return "listar_funcionarios"

    # Fallbacks inteligentes caso haja entidade mas sem verbos de ação explícitos
    if has_name:
        # Se mencionou um nome, provavelmente quer buscar ou ver dados do funcionário
        if any(d in text for d in ["dados", "detalhes", "completo", "ficha"]):
            return "dados_completos"
        return "buscar_funcionario"
        
    if has_department:
        return "listar_por_setor"
        
    if has_cargo:
        return "listar_por_cargo"

    return "unknown"
