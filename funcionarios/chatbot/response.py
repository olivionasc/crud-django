import random
from funcionarios.models import Funcionario

def format_currency(value) -> str:
    """Format float/decimal value to BRL currency string (e.g., R$ 5.430,00)."""
    try:
        val = float(value)
        return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return f"R$ {value}"


def format_date(date_val) -> str:
    """Format Date to DD/MM/YYYY."""
    if not date_val:
        return ""
    return date_val.strftime("%d/%m/%Y")


def get_display_name(field_name, value) -> str:
    """Gets the display name of a Choice field in the Funcionario model."""
    if not value:
        return ""
    choices_dict = {
        'departamento': dict(Funcionario.DEPARTAMENTO_CHOICES),
        'escolaridade': dict(Funcionario.ESCOLARIDADE_CHOICES),
        'tipo_contrato': dict(Funcionario.CONTRATO_CHOICES),
        'modelo_trabalho': dict(Funcionario.MODELO_TRABALHO_CHOICES),
    }
    
    dict_to_search = choices_dict.get(field_name, {})
    return dict_to_search.get(value.lower(), value)


def format_funcionario_details(f: Funcionario) -> str:
    """Gera uma formatação legível e estruturada para os detalhes de um funcionário."""
    status = "Ativo" if f.ativo else "Inativo"
    dept = get_display_name('departamento', f.departamento)
    escolaridade = get_display_name('escolaridade', f.escolaridade)
    contrato = get_display_name('tipo_contrato', f.tipo_contrato)
    modelo = get_display_name('modelo_trabalho', f.modelo_trabalho)
    salario = format_currency(f.salario)
    admissao = format_date(f.data_admissao)
    nascimento = format_date(f.data_nascimento)

    return (
        f"Encontrei as informações de **{f.nome}**:\n\n"
        f"• **Cargo:** {f.cargo}\n"
        f"• **Setor/Departamento:** {dept}\n"
        f"• **Salário:** {salario}\n"
        f"• **Data de Admissão:** {admissao}\n"
        f"• **Modelo de Trabalho:** {modelo} ({contrato})\n"
        f"• **Cidade:** {f.cidade}\n"
        f"• **Contato:** {f.telefone} | {f.email}\n"
        f"• **Data de Nascimento:** {nascimento}\n"
        f"• **Escolaridade:** {escolaridade}\n"
        f"• **Status:** {status}"
    )


def generate_response(query_result: dict) -> str:
    """
    Gera uma resposta amigável e em português com base nos resultados da consulta
    e nos templates predefinidos.
    """
    intent = query_result["intent"]
    entities = query_result["entities"]
    data = query_result["data"]
    dtype = query_result["type"]

    # Caso não tenhamos encontrado nenhum dado
    if dtype == 'empty':
        if intent in ['buscar_funcionario', 'dados_completos']:
            name = entities.get('name', 'o colaborador')
            return random.choice([
                f"Desculpe, não encontrei nenhum funcionário com o nome '{name}'. Verifique a grafia e tente novamente.",
                f"Não localizei '{name}' em nosso banco de dados. Tem certeza de que o nome está correto?",
                f"Busquei por '{name}', mas nenhum registro foi encontrado."
            ])
        else:
            return random.choice([
                "Não encontrei nenhum funcionário que atenda a esses critérios no momento.",
                "Não há registros no banco de dados correspondentes a essa solicitação.",
                "Nenhum colaborador correspondeu à sua pesquisa."
            ])

    # 1. Média Salarial
    if intent == 'media_salarial':
        val_formatted = format_currency(data)
        if entities.get('department'):
            dept_name = get_display_name('departamento', entities['department'])
            return random.choice([
                f"A média salarial no departamento de {dept_name} é de {val_formatted}.",
                f"O salário médio dos colaboradores do setor de {dept_name} é {val_formatted}.",
                f"No {dept_name}, a remuneração média está em {val_formatted}."
            ])
        else:
            return random.choice([
                f"O salário médio na empresa é de {val_formatted}.",
                f"A média salarial geral dos funcionários é atualmente {val_formatted}.",
                f"Atualmente, a média salarial da empresa está em {val_formatted}."
            ])

    # 2. Maior Salário
    elif intent == 'maior_salario':
        f = data
        sal_formatted = format_currency(f.salario)
        dept_name = get_display_name('departamento', f.departamento)
        if entities.get('department'):
            return random.choice([
                f"No setor de {dept_name}, o maior salário é de **{f.nome}** (cargo: {f.cargo}), que recebe {sal_formatted}.",
                f"O maior salário do departamento de {dept_name} pertence a **{f.nome}** ({f.cargo}), com uma remuneração de {sal_formatted}."
            ])
        else:
            return random.choice([
                f"**{f.nome}** ({f.cargo} no setor {dept_name}) possui o maior salário da empresa, recebendo {sal_formatted}.",
                f"O maior salário cadastrado é de **{f.nome}** (cargo: {f.cargo}), com {sal_formatted}.",
                f"Quem recebe a maior remuneração na empresa é **{f.nome}** ({f.cargo}), ganhando {sal_formatted}."
            ])

    # 3. Menor Salário
    elif intent == 'menor_salario':
        f = data
        sal_formatted = format_currency(f.salario)
        dept_name = get_display_name('departamento', f.departamento)
        if entities.get('department'):
            return random.choice([
                f"No setor de {dept_name}, a menor remuneração é de **{f.nome}** ({f.cargo}), que recebe {sal_formatted}.",
                f"O menor salário do setor {dept_name} pertence a **{f.nome}** ({f.cargo}), recebendo {sal_formatted}."
            ])
        else:
            return random.choice([
                f"**{f.nome}** ({f.cargo} no setor {dept_name}) possui o menor salário cadastrado, recebendo {sal_formatted}.",
                f"O menor salário da empresa é o de **{f.nome}** ({f.cargo}), com {sal_formatted}.",
                f"A menor remuneração registrada é de **{f.nome}** (cargo: {f.cargo}), no valor de {sal_formatted}."
            ])

    # 4. Contar Funcionários
    elif intent == 'contar_funcionarios':
        count = data
        dept = entities.get('department')
        active = entities.get('active')
        
        if dept and active is not None:
            dept_name = get_display_name('departamento', dept)
            status_str = "ativos" if active else "inativos"
            return f"Existem {count} funcionários {status_str} no setor de {dept_name}."
        elif dept:
            dept_name = get_display_name('departamento', dept)
            return random.choice([
                f"Encontrei {count} funcionários no setor de {dept_name}.",
                f"Temos {count} colaboradores cadastrados no departamento de {dept_name}.",
                f"O setor de {dept_name} conta atualmente com {count} colaboradores."
            ])
        elif active is not None:
            status_str = "ativos" if active else "inativos"
            return random.choice([
                f"Temos {count} funcionários {status_str} no momento.",
                f"O total de colaboradores {status_str} é de {count}.",
                f"Localizei {count} funcionários com status {status_str}."
            ])
        else:
            return random.choice([
                f"Existem {count} funcionários cadastrados no sistema.",
                f"O total de colaboradores cadastrados é de {count}.",
                f"Atualmente, o sistema possui {count} funcionários registrados."
            ])

    # 5. Contratado Recentemente
    elif intent == 'contratado_recentemente':
        if isinstance(data, list):
            # Caso em que o ano foi especificado
            year = entities.get('year')
            lines = [f"• **{f.nome}** - Cargo: {f.cargo} (Admissão: {format_date(f.data_admissao)})" for f in data]
            list_str = "\n".join(lines)
            return f"Encontrei {len(data)} funcionários contratados em {year}:\n\n{list_str}"
        else:
            f = data
            admissao = format_date(f.data_admissao)
            return random.choice([
                f"O funcionário contratado mais recentemente é **{f.nome}** ({f.cargo}), admitido em {admissao}.",
                f"A contratação mais recente da empresa é a de **{f.nome}** ({f.cargo}), que entrou em {admissao}.",
                f"**{f.nome}** ({f.cargo}) é o colaborador mais novo em termos de contratação (admitido em {admissao})."
            ])

    # 6. Contratado há Mais Tempo
    elif intent == 'contratado_antigamente':
        f = data
        admissao = format_date(f.data_admissao)
        return random.choice([
            f"O funcionário contratado há mais tempo é **{f.nome}** ({f.cargo}), admitido em {admissao}.",
            f"Quem foi admitido primeiro na empresa foi **{f.nome}** ({f.cargo}), em {admissao}.",
            f"**{f.nome}** ({f.cargo}) é a contratação mais antiga da empresa (admitido em {admissao})."
        ])

    # 7. Buscar Funcionário / Dados Completos
    elif intent in ['buscar_funcionario', 'dados_completos']:
        return format_funcionario_details(data)

    # 8. Listas (Geral, Setor, Cargo, etc.)
    elif intent in ['listar_por_setor', 'listar_por_cargo', 'listar_funcionarios'] or dtype == 'list':
        funcs = data
        lines = []
        for i, f in enumerate(funcs, 1):
            dept_name = get_display_name('departamento', f.departamento)
            lines.append(f"{i}. **{f.nome}** — {f.cargo} ({dept_name})")
        
        list_str = "\n".join(lines)
        
        if intent == 'listar_por_setor' and entities.get('department'):
            dept_name = get_display_name('departamento', entities['department'])
            title = f"Funcionários no setor de **{dept_name}** ({len(funcs)} encontrados):"
        elif intent == 'listar_por_cargo' and entities.get('cargo'):
            title = f"Funcionários com cargo de **{entities['cargo']}** ({len(funcs)} encontrados):"
        else:
            title = f"Lista de funcionários ({len(funcs)} cadastrados):"

        return f"{title}\n\n{list_str}"

    return "Desculpe, processou a consulta com sucesso mas não sei como formular essa resposta."
