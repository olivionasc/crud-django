from django.db.models import Count, Avg
from funcionarios.models import Funcionario
from .response import format_currency, get_display_name

def build_dashboard() -> dict:
    """
    Constrói a estrutura de dados consolidada para o Dashboard Completo.
    """
    # 1. KPIs
    total = Funcionario.objects.count()
    ativos = Funcionario.objects.filter(ativo=True).count()
    inativos = Funcionario.objects.filter(ativo=False).count()

    avg_salary = Funcionario.objects.aggregate(avg=Avg('salario'))['avg'] or 0.0
    max_f = Funcionario.objects.order_by('-salario').first()
    min_f = Funcionario.objects.order_by('salario').first()

    max_val = f"{format_currency(max_f.salario)} - {max_f.nome}" if max_f else "N/A"
    min_val = f"{format_currency(min_f.salario)} - {min_f.nome}" if min_f else "N/A"

    kpis = [
        {"type": "kpi", "title": "Total de Funcionários", "value": total},
        {"type": "kpi", "title": "Funcionários Ativos", "value": ativos},
        {"type": "kpi", "title": "Funcionários Inativos", "value": inativos},
        {"type": "kpi", "title": "Salário Médio", "value": format_currency(avg_salary)},
        {"type": "kpi", "title": "Maior Salário", "value": max_val},
        {"type": "kpi", "title": "Menor Salário", "value": min_val},
    ]

    # 2. Gráficos
    # A. Funcionários por setor
    setores_query = Funcionario.objects.values('departamento').annotate(val=Count('id')).order_by('departamento')
    setores_labels = [get_display_name('departamento', item['departamento']) for item in setores_query]
    setores_values = [item['val'] for item in setores_query]
    chart_setores = {
        "type": "bar-chart",
        "title": "Funcionários por Setor",
        "data": {
            "labels": setores_labels,
            "datasets": [{"label": "Quantidade", "data": setores_values}]
        }
    }

    # B. Funcionários por cargo
    cargos_query = Funcionario.objects.values('cargo').annotate(val=Count('id')).order_by('-val')[:5]
    cargos_labels = [item['cargo'] for item in cargos_query]
    cargos_values = [item['val'] for item in cargos_query]
    chart_cargos = {
        "type": "bar-chart",
        "title": "Funcionários por Cargo (Top 5)",
        "data": {
            "labels": cargos_labels,
            "datasets": [{"label": "Quantidade", "data": cargos_values}]
        }
    }

    # C. Distribuição salarial (Média por Setor)
    salarios_query = Funcionario.objects.values('departamento').annotate(val=Avg('salario')).order_by('departamento')
    salarios_labels = [get_display_name('departamento', item['departamento']) for item in salarios_query]
    salarios_values = [float(item['val'] or 0.0) for item in salarios_query]
    chart_salarios = {
        "type": "pie-chart",
        "title": "Distribuição Salarial Média por Setor",
        "data": {
            "labels": salarios_labels,
            "datasets": [{"label": "Média (R$)", "data": salarios_values}]
        }
    }

    # D. Contratações por mês/ano
    funcionarios = Funcionario.objects.all().order_by('data_admissao')
    months_map = {}
    for f in funcionarios:
        key = f.data_admissao.strftime("%m/%Y")
        months_map[key] = months_map.get(key, 0) + 1

    def parse_key(k):
        parts = k.split('/')
        return int(parts[1]), int(parts[0])

    sorted_keys = sorted(months_map.keys(), key=parse_key)
    chart_contratacoes = {
        "type": "line-chart",
        "title": "Contratações por Mês/Ano",
        "data": {
            "labels": sorted_keys,
            "datasets": [{"label": "Contratações", "data": [months_map[k] for k in sorted_keys]}]
        }
    }

    return {
        "type": "dashboard",
        "title": "Dashboard Geral de Indicadores",
        "components": kpis + [chart_setores, chart_cargos, chart_salarios, chart_contratacoes]
    }
