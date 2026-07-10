from django.db.models import Avg
from funcionarios.models import Funcionario

def execute_query(intent: str, entities: dict) -> dict:
    """
    Executa a consulta apropriada no banco de dados usando o Django ORM
    com base na intenção e entidades extraídas.
    """
    result = {
        "intent": intent,
        "entities": entities,
        "data": None,
        "type": "empty"  # 'list', 'single', 'value', 'empty'
    }

    queryset = Funcionario.objects.all()

    # Aplicar filtros globais se presentes nas entidades
    if entities.get('active') is not None:
        queryset = queryset.filter(ativo=entities['active'])
    
    if entities.get('department'):
        queryset = queryset.filter(departamento=entities['department'])
        
    if entities.get('cargo'):
        queryset = queryset.filter(cargo__iexact=entities['cargo'])
        
    if entities.get('year'):
        queryset = queryset.filter(data_admissao__year=entities['year'])
        
    if entities.get('salary_value') is not None:
        val = entities['salary_value']
        op = entities['salary_operator']
        if op == 'greater':
            queryset = queryset.filter(salario__gt=val)
        elif op == 'less':
            queryset = queryset.filter(salario__lt=val)
        else:
            queryset = queryset.filter(salario=val)

    # Executar consultas específicas por intenção
    if intent == 'media_salarial':
        avg = queryset.aggregate(media=Avg('salario'))['media']
        result['data'] = avg or 0.0
        result['type'] = 'value'

    elif intent == 'maior_salario':
        func = queryset.order_by('-salario').first()
        result['data'] = func
        result['type'] = 'single' if func else 'empty'

    elif intent == 'menor_salario':
        func = queryset.order_by('salario').first()
        result['data'] = func
        result['type'] = 'single' if func else 'empty'

    elif intent == 'contar_funcionarios':
        count = queryset.count()
        result['data'] = count
        result['type'] = 'value'

    elif intent == 'contratado_recentemente':
        # Se filtrou por ano (ex: "este ano"), retorna a lista de contratados naquele período
        if entities.get('year'):
            funcs = list(queryset.order_by('-data_admissao'))
            result['data'] = funcs
            result['type'] = 'list' if funcs else 'empty'
        else:
            func = queryset.order_by('-data_admissao').first()
            result['data'] = func
            result['type'] = 'single' if func else 'empty'

    elif intent == 'contratado_antigamente':
        func = queryset.order_by('data_admissao').first()
        result['data'] = func
        result['type'] = 'single' if func else 'empty'

    elif intent in ['buscar_funcionario', 'dados_completos']:
        name = entities.get('name')
        if name:
            # Tenta buscar pelo nome exato primeiro
            func = Funcionario.objects.filter(nome__iexact=name).first()
            if not func:
                # Fallback para busca de parte do nome
                func = Funcionario.objects.filter(nome__icontains=name).first()
            result['data'] = func
            result['type'] = 'single' if func else 'empty'
        else:
            result['type'] = 'empty'

    elif intent in ['listar_por_setor', 'listar_por_cargo', 'listar_funcionarios']:
        funcs = list(queryset.order_by('nome'))
        result['data'] = funcs
        result['type'] = 'list' if funcs else 'empty'

    else:
        # Se a intenção for desconhecida mas houver filtros ativos, lista os correspondentes
        funcs = list(queryset.order_by('nome'))
        result['data'] = funcs
        result['type'] = 'list' if funcs else 'empty'

    return result
